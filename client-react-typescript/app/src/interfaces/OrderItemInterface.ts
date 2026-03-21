import type { Product } from "./ProductInterface.ts";

export interface OrderItem {
    product: Product,
    price: number,
    amount: number
}