import { ITSList } from "../interfaces/generic";
import ProblemItem from "./problemItem";
interface props {
  problemList: ITSList[];
}

function ProblemList({ problemList }: props) {
  return (
    <div>
      {problemList?.map((tsStep: ITSList) => (
        <ProblemItem tsStep={tsStep}></ProblemItem>
      ))}
    </div>
  );
}

export default ProblemList;
