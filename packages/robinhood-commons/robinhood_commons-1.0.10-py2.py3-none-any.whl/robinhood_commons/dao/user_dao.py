import csv
from typing import Dict, List

import pyotp

from robinhood_commons.entity.printable import Printable
from robinhood_commons.entity.user import User
from robinhood_commons.util.constants import BASE_PATH

PATH: str = f'{BASE_PATH}/users.csv'


class UserDao(Printable):

    @staticmethod
    def get_users(path: str = PATH) -> List[User]:
        users: List[User] = []
        first: bool = True
        with open(path) as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if first:
                    first = False
                    continue

                mfa_code = row[3] if len(row) >= 4 and row[3] not in ['', None] else None
                users.append(User(username=row[0], email=row[1], pwd=row[2], mfa_code=mfa_code))
        return users

    @staticmethod
    def get_users_by_email() -> Dict[str, User]:
        return {u.email: u for u in UserDao.get_users()}
        # return next((user for user in UserDao.get_users() if user.email == email), None)

    @staticmethod
    def get_user_by_email(email: str) -> User:
        return UserDao.get_users_by_email()[email]


def main() -> None:
    user_dao = UserDao()
    print(user_dao.get_users())
    print(user_dao.get_users_by_email())

    print(f'MFA: {pyotp.TOTP(user_dao.get_users()[0].mfa_code).now()}')


if __name__ == '__main__':
    main()
