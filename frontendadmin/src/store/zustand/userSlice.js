export const createUserSlice = (set) => ({
  resourceGroup: null,
  userName: "",
  token: null,
  setToken: (token) => set(() => ({ token })),
  setResourceGroup: (rg) => set(() => ({ resourceGroup: rg })),
});
