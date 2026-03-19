import React from "react"
import OrderPaymentStatusBox from "../components/order-payment-status-box.jsx";
import { createPortal } from "react-dom";

export default function TestPage() {
    return (
        createPortal(
            <OrderPaymentStatusBox
                orderId = {'826ce587-36f9-4de4-8bfd-423645e256f2'}
                paymentStatus = {'successful'}
            />,
            document.body
        )
    )
}