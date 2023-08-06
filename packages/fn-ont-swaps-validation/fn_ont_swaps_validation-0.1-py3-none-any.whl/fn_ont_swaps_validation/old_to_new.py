import logging

from dataclasses import dataclass
from fibrenest_db_models.postgres import ONT, SUBSCRIPTION
from fibrenest_db_models.old import Service, Base as OLDBase
from sqlalchemy import Column, BigInteger, Text, DateTime
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from concurrent.futures import ThreadPoolExecutor
from fn_ont_swaps_validation.exceptions import ValidationError, CantProceedError


class RADACCT(OLDBase):
    __tablename__ = 'radacct'

    radacctid = Column(BigInteger, primary_key=True)
    username = Column(Text)
    realm = Column(Text)
    acctstoptime = Column(DateTime(True))


@dataclass(eq=False)
class OltToNewValidation:
    old_ont: str
    new_ont: str
    logger: logging.Logger
    old_db_session: Session
    old_db_radius_session: Session
    new_db_session: Session

    def _validate_old(self):
        """ Validates OLD ONT """

        try:
            self.logger.info(f'Validating old ont: {self.old_ont} for old to new ont swap')
            old_ont_data = self.old_db_session.query(Service).filter(Service.pon == self.old_ont).one()
            if old_ont_data.cust_id \
                    and (
                    old_ont_data.ppp_prov_state == 'PPP_DETAILS_SET'
                    or old_ont_data.ppp_prov_state == 'RADIUS_RECORD_CREATED'
            ):
                self.logger.info(f'Checking that there is no active session for a customer on old ont: {self.old_ont}')
                old_radacct = self.old_db_radius_session.query(RADACCT).filter(
                    RADACCT.username == f'{old_ont_data.cust_id}@hsi.fibrenest.net'
                ).order_by(RADACCT.radacctid.desc()).first()
                if old_radacct and old_radacct.acctstoptime is None:
                    error_msg = f'There seems to be an online session for old ont: {self.old_ont}'
                    self.logger.error(error_msg)
                    raise ValidationError(error_msg)
        except NoResultFound as no_result_error:
            raise ValidationError(f'Validation failed for old ont: {self.old_ont}. No DB record') from no_result_error
        except MultipleResultsFound as multi_result_error:
            raise ValidationError(
                f'Validation failed for old ont: {self.old_ont}. Multiple DB record') from multi_result_error

    def _validate_new(self):
        """ Validates NEW ONT """

        try:
            self.logger.info(f'Validating new ont: {self.new_ont} for old to new ont swap')
            new_ont_data = self.new_db_session.query(ONT).filter(ONT.sn == self.new_ont).one()
            if not new_ont_data.ont_registered:
                msg = f'Cannot proceed until the new ont: {self.new_ont} is registered'
                raise CantProceedError(msg)

            self.logger.info(f'Checking is there is already a subscription provided on new ont: {self.new_ont}')
            sub_on_new_ont = self.new_db_session.query(SUBSCRIPTION).filter(
                SUBSCRIPTION.ont_id == new_ont_data.id).one_or_none()
            if sub_on_new_ont:
                error_msg = f'There is a subscription, subs_id: {sub_on_new_ont.subs_id} on new ont: {self.new_ont}'
                self.logger.error(error_msg)
                raise ValidationError(error_msg)
        except NoResultFound as no_result_error:
            raise ValidationError(f'Validation failed for new ont: {self.new_ont}. No DB record') from no_result_error
        except MultipleResultsFound as multi_result_error:
            raise ValidationError(
                f'Validation failed for new ont: {self.new_ont}. Multiple DB record') from multi_result_error

    def validate_old_to_new_swap(self):
        """
        Performs some validation like checking the ONTs still exists in DB and service status hasn't changed
        :return: None
        :raise ValidationError: If any validation error
        :raise CantProceedError: If we cant proceed with the swap. This isn't an error as such
        """

        with ThreadPoolExecutor(max_workers=2) as executor:
            old_validate = executor.submit(self._validate_old)
            new_validate = executor.submit(self._validate_new)
            old_exception = old_validate.exception()
            new_exception = new_validate.exception()

        if old_exception:
            raise old_exception

        if new_exception:
            raise new_exception

        return None
