import { ITSList } from "../interfaces/generic";
interface props {
  tsStep: ITSList;
}

function ProblemItem({ tsStep }: props) {
  return <h1>{tsStep.problem}</h1>;
}

export default ProblemItem;
