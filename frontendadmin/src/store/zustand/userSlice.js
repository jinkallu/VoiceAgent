export const createUserSlice = (set) => ({
  resourceGroup: null,
  userName: "",
  token: null,
  isLoggedIn: false,
  setIsLoggedIn: (val) => set(() => ({ isLoggedIn: val })),
  setUserName: (val) => set(() => ({ userName: val })),
  setToken: (token) => set(() => ({ token })),
  setResourceGroup: (rg) => set(() => ({ resourceGroup: rg })),
});
