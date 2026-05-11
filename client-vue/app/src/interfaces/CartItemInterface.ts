import type { Product } from "./ProductInterface.ts";

export interface CartItem {
    id: string,
    amount: number,
    product: Product
}