import { useState } from "react";
import { IStep, ITSList } from "../interfaces/generic";
import Button from "./UI/button/Button";

function NewProblem() {
  const [tsStep, setTSStep] = useState<ITSList>();
  const [steps, setSteps] = useState<IStep[]>([]);
  const [problem, setProblem] = useState("");
  const [step, setStep] = useState("");
  const addProblem = (problem: string) => {
    setTSStep((prev) => {
      return { problem, steps: prev?.steps || [] };
    });
  };

  // const addProblemStep = (step: string) => {
  //   steps.push({step,resource:{}})
  // };

  return (
    <div>
      <div>
        <input
          placeholder="Problem"
          name="problem"
          onChange={(e) => setProblem(e.target.value)}
        ></input>
        <Button onClick={() => addProblem(problem)}>Add Problem</Button>
        <input
          placeholder="Add step"
          value={step}
          onChange={(e) => setStep(e.target.value)}
        ></input>
        <Button onClick={() => {}}>Add step</Button>
      </div>

      {tsStep?.problem && (
        <div>
          <h3>Problem - {tsStep.problem}</h3>
          {tsStep?.steps?.map((step) => (
            <h3>{step}</h3>
          ))}
        </div>
      )}
    </div>
  );
}

export default NewProblem;
