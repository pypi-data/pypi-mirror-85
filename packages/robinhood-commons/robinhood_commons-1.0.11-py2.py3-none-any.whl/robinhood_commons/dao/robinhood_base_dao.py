import pyotp
import robin_stocks as rh

from robinhood_commons.dao.user_dao import UserDao
from robinhood_commons.entity.user import User
from robinhood_commons.util.constants import MAIN_EMAIL, PROFILE_INFO


class RobinhoodBaseDao:

    def __init__(self, a_user: User) -> None:
        try:
            profile = rh.load_basic_profile()
            if PROFILE_INFO:
                print(f'Basic Profile: {profile}')
        except Exception as e:
            print(e)

            if a_user.mfa_code is None:
                rh.login(username=a_user.username, password=a_user.pwd, store_session=True)
            else:
                mfa_code = pyotp.TOTP(a_user.mfa_code).now()
                rh.login(username=a_user.username, password=a_user.pwd, store_session=True, mfa_code=mfa_code)

    @classmethod
    def logout(cls) -> None:
        rh.logout()


if __name__ == '__main__':
    user: User = UserDao.get_user_by_email(email=MAIN_EMAIL)

    dao = RobinhoodBaseDao(user)
    print(dao)
