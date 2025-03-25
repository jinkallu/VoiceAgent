import { create } from "zustand";
import { createUserSlice } from "./userSlice";
import { createProductSlice } from "./productSlice";

export const useAdminStore = create((...a) => ({
  ...createUserSlice(...a),
  ...createProductSlice(...a),
}));
