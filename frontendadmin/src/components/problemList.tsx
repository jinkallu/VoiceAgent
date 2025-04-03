import { Icon } from "@iconify/react";
import { ITSList } from "../interfaces/generic";
import ProblemItem from "./problemItem";
interface props {
  problemList: ITSList[];
  productName: string;
  editable: boolean;
  deleteProblem: (val: string) => void;
  openEditProblem: (val: ITSList) => void;
}

function ProblemList({
  problemList,
  productName,
  editable,
  deleteProblem,
  openEditProblem,
}: props) {
  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        width: "100%",
      }}
    >
      {problemList?.map((tsStep: ITSList) => (
        <div
          key={tsStep.problem}
          style={{
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
            width: "100%",
            boxShadow: "2px 2px gray",
            borderLeft: "2px solid lightblue",
          }}
        >
          <ProblemItem
            key={tsStep.problem}
            tsStep={tsStep}
            productName={productName}
          ></ProblemItem>
          <div style={{ display: "flex", alignItems: "center", gap: "2px" }}>
            {editable && (
              <Icon
                width={32}
                height={32}
                onClick={() => deleteProblem(tsStep.problem)}
                icon="material-symbols:delete-outline"
              ></Icon>
            )}
            {editable && (
              <Icon
                width={32}
                height={32}
                onClick={() => openEditProblem(tsStep)}
                icon="mingcute:edit-line"
              ></Icon>
            )}
          </div>
        </div>
      ))}
    </div>
  );
}

export default ProblemList;
