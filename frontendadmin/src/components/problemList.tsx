import { ITSList } from "../interfaces/generic";
import ProblemItem from "./problemItem";
interface props {
  problemList: ITSList[];
  productName: string;
  editable: boolean;
}

function ProblemList({ problemList, productName, editable }: props) {
  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
      }}
    >
      {problemList?.map((tsStep: ITSList) => (
        <ProblemItem
          key={tsStep.problem}
          tsStep={tsStep}
          productName={productName}
        ></ProblemItem>
      ))}
    </div>
  );
}

export default ProblemList;
