import { useEffect, useState } from "react";
import { IStep, ITSList } from "../interfaces/generic";
import Button from "./UI/button/Button";
import { Icon } from "@iconify/react";
interface props {
  addTSStep: (val: ITSList) => void;
  setNewProblem: (val: boolean) => void;
  data?: ITSList | null;
}

function NewProblem({ addTSStep, setNewProblem, data }: props) {
  const [tsStep, setTSStep] = useState<ITSList>();
  // const [steps, setSteps] = useState<IStep[]>([]);
  const [problem, setProblem] = useState("");
  const [step, setStep] = useState<string>("");
  const addProblem = (problem: string) => {
    setTSStep((prev) => {
      return { problem, steps: prev?.steps || [] };
    });
  };

  const saveTSStep = (tsStep: ITSList | null) => {
    if (tsStep) {
      addTSStep(tsStep);
      setNewProblem(false);
    }
  };
  const removeStep = (step: string) => {
    const newSteps = tsStep?.steps?.filter((item) => item.step !== step);
    setTSStep({ problem: tsStep?.problem || "", steps: newSteps || [] });
  };

  const addProblemStep = (step: string) => {
    if (!tsStep?.problem || !step) return;
    // setSteps((prev) => [...prev, { step, resource: null }]);
    const isStepExisting = tsStep?.steps.filter((item) => item.step === step);
    if (isStepExisting.length > 0) {
      return;
    }
    const newTSStep: ITSList = {
      problem: tsStep.problem || "",
      steps: [...tsStep?.steps, { step, resource: null }],
    };

    setTSStep((prev) => {
      return newTSStep;
    });
    setStep("");
  };
  useEffect(() => {
    if (data) setTSStep(data);
  }, [data]);

  return (
    <div
      style={{
        boxShadow: "2px lightblue",
        display: "flex",
        flexDirection: "column",
        minHeight: "60vh",
        overflowY: "auto",
      }}
    >
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          marginBottom: "5px",
        }}
      >
        <textarea
          style={{
            minWidth: "500px",
            maxWidth: "100%",
            minHeight: "50px",
            height: "100%",
            width: "100%",
          }}
          placeholder="Problem"
          name="problem"
          onChange={(e) => setProblem(e.target.value)}
          defaultValue={data?.problem}
        ></textarea>
        <Button onClick={() => addProblem(problem)}>Add Problem</Button>
      </div>
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
        }}
      >
        <textarea
          style={{
            minWidth: "500px",
            maxWidth: "100%",
            minHeight: "50px",
            height: "100%",
            width: "100%",
          }}
          placeholder="Add step"
          value={step}
          onChange={(e) => setStep(e.target.value)}
        ></textarea>
        <Button onClick={() => addProblemStep(step)}>Add step</Button>
      </div>

      {tsStep?.problem && (
        <div
          style={{
            display: "flex",
            flexDirection: "column",
            marginTop: "10px",
            marginBottom: "10px",
          }}
        >
          <h3>Problem - {tsStep.problem}</h3>
          <h4>Steps</h4>
          {tsStep?.steps?.map((step, index) => (
            <div
              style={{
                display: "flex",
                justifyContent: "space-between",
                alignItems: "center",
                boxShadow: "2px 2px lightblue",
                padding: "5px",
              }}
              key={step.step}
            >
              <div
                style={{ display: "flex", alignItems: "center", gap: "5px" }}
              >
                <h5>{index + 1}.</h5>
                <h5>{step.step}</h5>
              </div>

              <Icon
                onClick={() => removeStep(step.step)}
                icon="material-symbols-light:delete-outline"
              ></Icon>
            </div>
          ))}
        </div>
      )}
      <div
        style={{
          display: "flex",
          justifyContent: "flex-end",
          alignItems: "center",
          marginTop: "20px",
        }}
      >
        <Button onClick={() => setNewProblem(false)} outline={true}>
          Cancel
        </Button>
        {!tsStep && <Button disabled={!tsStep} onClick={() => {}} />}
        {tsStep?.problem && tsStep?.steps.length > 0 && (
          <Button disabled={!tsStep} onClick={() => saveTSStep(tsStep)}>
            Save
          </Button>
        )}
      </div>
    </div>
  );
}

export default NewProblem;
