import React from "react";
import { useTranslation } from "react-i18next";
import { Link, useLocation } from "react-router-dom";
import { Icon } from "@iconify/react";
import Summary from "../components/summary/Summary";
import SaleChart from "../components/chart/Chart";

function Dashboard() {
  const { t } = useTranslation();
  return (
    <section>
      <h2 className="title">{t("dashboard")}</h2>
      <Link
          to={`assistant`}
        >
          <div>
            <Icon icon={""} />
          </div>
          <div >Assistant</div>
        </Link>
      <Summary />
      <SaleChart />
    </section>
  );
}

export default Dashboard;
