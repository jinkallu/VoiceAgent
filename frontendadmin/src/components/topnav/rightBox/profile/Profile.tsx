import { Icon } from "@iconify/react";
import { images } from "../../../../constants";
import { useAdminStore } from "../../../../store/zustand/store";
import classes from "./Profile.module.scss";
import { useTranslation } from "react-i18next";

function Profile() {
  const { t } = useTranslation();
  const userName = useAdminStore((state) => state.userName);

  return (
    <div className={classes.profile}>
      <div
        style={{
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          gap: "10px",
          borderRadius: "50%",
        }}
      >
        <Icon width={40} height={40} icon="icon-park-outline:avatar"></Icon>
      </div>
      <div className={classes.profile__info}>
        <p className={classes.profile__userName}>{userName}</p>
        {/* <span className={classes.profile__role}>{t("admin")}</span> */}
      </div>
    </div>
  );
}

export default Profile;
