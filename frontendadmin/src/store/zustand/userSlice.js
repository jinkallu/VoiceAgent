export const createUserSlice = (set) => ({
  resourceGroup: null,
  userName: "",
  token: null,
  isLoggedIn: false,
  setIsLoggedIn: (val) => set(() => ({ isLoggedIn: val })),
  setToken: (token) => set(() => ({ token })),
  setResourceGroup: (rg) => set(() => ({ resourceGroup: rg })),
});
