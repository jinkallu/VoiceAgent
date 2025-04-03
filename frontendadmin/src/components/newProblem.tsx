import { useEffect, useState } from "react";
import { IStep, ITSList } from "../interfaces/generic";
import Button from "./UI/button/Button";
import { Icon } from "@iconify/react";
import ResourceItem from "./resourceItem";
import { removeResource, uploadImage } from "../services/apiService";
import { useAdminStore } from "../store/zustand/store";
import Modal from "./UI/modal/Modal";
import ImageHandler from "./imageHandler";
interface props {
  addTSStep: (val: ITSList) => void;
  setNewProblem: (val: boolean) => void;
  data?: ITSList | null;
  productName: string | "";
}

function NewProblem({ productName, addTSStep, setNewProblem, data }: props) {
  const [tsStep, setTSStep] = useState<ITSList>();
  // const [steps, setSteps] = useState<IStep[]>([]);
  const [isAddImageOpen, setIsAddImageOpen] = useState<boolean>(false);
  const [problem, setProblem] = useState("");
  const [step, setStep] = useState<string>("");
  const token = useAdminStore((state) => state.token);
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
  const uploadSelectedImage = async (
    formData: FormData,
    fileName: string,
    step: string
  ) => {
    formData.append("product_name", productName);
    const res = await uploadImage(token, formData);
    if (res === true) {
      const newTSList = { ...tsStep };
      const newSteps = newTSList?.steps?.map((item) => {
        if (item.step === step) {
          return { ...item, resource: { type: "image", fileName: fileName } };
        }

        return item;
      });
      console.log(newSteps);

      if (tsStep?.problem) {
        const newTSStep = { ...tsStep, steps: newSteps || [] };
        setTSStep(newTSStep);

        addTSStep(newTSStep);
      }

      console.log(res);
    }
    setIsAddImageOpen(false);
  };
  const removeResourceFromStep = async (
    token: string,
    problem: string,
    step: string,
    productName: string,
    resource: any
  ) => {
    const newTSList = { ...tsStep };
    const newSteps = newTSList?.steps?.map((item) => {
      if (item.step === step) {
        return { ...item, resource: null };
      }

      return item;
    });
    console.log(newSteps);

    if (tsStep?.problem) {
      const newTSStep = { ...tsStep, steps: newSteps || [] };
      setTSStep(newTSStep);

      addTSStep(newTSStep);
    }

    // removeResource(token, productName, resource);
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
      {tsStep?.problem && (
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
      )}

      {tsStep?.problem && (
        <div
          style={{
            display: "flex",
            flexDirection: "column",
            marginTop: "10px",
            marginBottom: "10px",
            height: "50vh",
            overflowY: "auto",
          }}
        >
          <h3>Problem - {tsStep.problem}</h3>
          <h4>Steps</h4>
          {tsStep?.steps?.map((step, index) => (
            <div
              style={{
                display: "flex",
                flexDirection: "column",

                boxShadow: "2px 2px lightblue",
              }}
              key={step.step}
            >
              <div
                style={{
                  display: "flex",
                  justifyContent: "space-between",
                  alignItems: "center",
                  padding: "5px",
                }}
              >
                <div
                  style={{ display: "flex", alignItems: "center", gap: "5px" }}
                >
                  <h5>{index + 1}.</h5>
                  <h5>{step.step}</h5>
                </div>
                <ResourceItem
                  productName={productName}
                  resource={step.resource}
                  expanded={true}
                ></ResourceItem>
              </div>
              <div
                style={{
                  display: "flex",
                  justifyContent: "end",
                  alignItems: "center",
                  gap: "10px",
                  paddingBottom: "5px",
                }}
              >
                <Button
                  outline
                  onClick={() =>
                    removeResourceFromStep(
                      token,
                      tsStep.problem,
                      step.step,
                      productName,
                      step.resource
                    )
                  }
                >
                  Remove Image
                </Button>
                <Button outline onClick={() => setIsAddImageOpen(true)}>
                  Change/Add Image
                </Button>

                <Button outline onClick={() => removeStep(step.step)}>
                  Remove Step
                </Button>
              </div>
              {isAddImageOpen && (
                <ImageHandler
                  step={step.step}
                  uploadSelectedImage={uploadSelectedImage}
                ></ImageHandler>
              )}
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
