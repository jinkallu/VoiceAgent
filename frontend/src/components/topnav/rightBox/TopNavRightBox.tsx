import React from "react";
import ThemeBox from "./themeBox/ThemeBox";
import Profile from "./profile/Profile";

import classes from "./TopNavRightBox.module.scss";

function TopNavRightBox() {
  return (
    <div className={classes.topNavBox_right}>
      <div className={classes.wrapper}>
        <ThemeBox />
      </div>
      <Profile />
    </div>
  );
}

export default TopNavRightBox;
