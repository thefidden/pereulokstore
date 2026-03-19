import type { OrderItem } from "./OrderItemInterface.ts";

export interface Order {
    id: string,
    date: string,
    price: number,
    status: string,
    items: Array<OrderItem>
}