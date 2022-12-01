from sqlalchemy import text
from db.connection import engine
from scheduler.domain.entities.user_setting import UserSetting


class UserSettingsRepository:
    def get_all(self) -> list[UserSetting]:
        with engine.begin() as connection:
            result = connection.execute(text("SELECT * FROM user_settings"))
            return [UserSetting(user_id=row.user_id) for row in result]

    def add_or_update(self, setting: UserSetting) -> None:
        with engine.begin() as connection:
            connection.execute(
                text(
                    "INSERT INTO user_settings (user_id) VALUES (:user_id) ON CONFLICT DO NOTHING"
                ),
                {"user_id": setting.user_id},
            )
