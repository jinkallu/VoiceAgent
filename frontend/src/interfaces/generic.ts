export interface ITSList {
  problem: string;
  steps: IStep[] | [];
}

export interface IStep {
  step: string;
  resource: IResource | null;
}
export interface IResource {
  type: string;
  fileName: string;
}

export interface IImage {
  val: FormData;
  fileName: string;
  step: string;
}
