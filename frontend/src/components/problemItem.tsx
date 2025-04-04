import { Icon } from "@iconify/react";
import { ITSList } from "../interfaces/generic";
import ResourceItem from "./resourceItem";
import { useState } from "react";
interface props {
  tsStep: ITSList;
  productName: string;
}

function ProblemItem({ tsStep, productName }: props) {
  const [expanded, setExpanded] = useState(false);
  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        padding: "5px",
        width: "100%",
      }}
    >
      <div
        style={{
          display: "flex",
          gap: "5px",
          marginBottom: "10px",
          marginTop: "10px",
        }}
      >
        <Icon
          style={{ cursor: "pointer" }}
          onClick={() => setExpanded((prev) => !prev)}
          icon={`${expanded ? "ep:minus" : "ep:plus"}`}
        ></Icon>
        <div
          style={{
            display: "flex",
            gap: "5px",
            justifyContent: "space-between",
            alignItems: "center",
            width: "100%",
          }}
        >
          <h4>{tsStep.problem}</h4>
          <div
            style={{
              borderRadius: "50%",
              display: "flex",
              justifyContent: "center",
              alignItems: "center",
              paddingLeft: "20px",
              marginLeft: "20px",
              padding: "4px",
              width: "24px",
              height: "24px",
              backgroundColor: "lightblue",
            }}
          >
            {tsStep?.steps?.length || 0}
          </div>
        </div>
      </div>
      {expanded && (
        <table
          style={{ tableLayout: "fixed", width: "100%", marginLeft: "25px" }}
        >
          <tbody>
            {tsStep?.steps?.map((item) => (
              <tr style={{ boxShadow: "2px 2px lightblue" }} key={item.step}>
                <td
                  style={{
                    width: "80%",
                    wordBreak: "break-all",
                    wordWrap: "break-word",
                    whiteSpace: "nowrap",
                  }}
                >
                  {item.step}
                </td>
                <td style={{ width: "100px" }}>
                  {item?.resource && (
                    <ResourceItem
                      resource={item.resource}
                      productName={productName}
                      expanded={expanded}
                    ></ResourceItem>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}

export default ProblemItem;
