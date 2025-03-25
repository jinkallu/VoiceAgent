export const createProductSlice = (set) => ({
  products: [],
  setProducts: (pd) => set(() => ({ products: pd })),
});
