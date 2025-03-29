export interface ITSList {
  problem: string;
  steps: IStep[];
}

export interface IStep {
  step: string;
  resource: IResource;
}
export interface IResource {
  type: string;
  fileName: string;
}
