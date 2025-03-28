export const createProductSlice = (set) => ({
  products: [],
  productData: [],
  currentResourceGroup: null,
  currentProduct: {},
  setProducts: (pd) => set(() => ({ products: pd })),
  setCurrentProduct: (pd) => set(() => ({ currentProduct: pd })),
  setProductData: (pd) => set(() => ({ productData: pd })),
  setCurrentResourceGroup: (pd) => set(() => ({ currentResourceGroup: pd })),
});
