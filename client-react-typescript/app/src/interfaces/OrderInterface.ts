import type { OrderItem } from "./OrderItemInterface.ts";

type OrderStatus =
    "pending_payment" |
    "paid" |
    "pending_assembly" |
    "assembled" |
    "pending_pickup" |
    "picked_up" |
    "finished" |
    "cancelled"

export interface Order {
    id: string,
    date: string,
    price: number,
    status: OrderStatus,
    items: Array<OrderItem>
}