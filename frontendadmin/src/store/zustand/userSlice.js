export const createUserSlice = (set) => ({
  resourceGroups: [],
  userName: "",
  token: null,
  setToken: (token) => set(() => ({ token })),
  setResourceGroups: (rg) => set(() => ({ resourceGroups: rg })),
});
