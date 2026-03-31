import { createPortal } from "react-dom";
import Loader from "../components/Loader.tsx";
import { useNavigate, useParams, useSearchParams } from "react-router-dom";
import { useAppDispatch, useAppSelector } from "../store.ts";
import { useEffect } from "react";
import { fetchOrderPaymentStatus } from "../slices/OrderPaymentStatus.tsx";
import { emptyCart } from "../slices/CartSlice.ts";

export default function OrderCheckPaymentPage() {
    const dispatch = useAppDispatch()
    const navigate = useNavigate()

    const { orderUUID: orderId } = useParams()
    const { orderId: bankOrderId } = Object.fromEntries(useSearchParams()[0])

    const {
        status: orderPaymentStatus
    } = useAppSelector(state => state.orderPaymentStatus)

    useEffect(() => {
        dispatch(fetchOrderPaymentStatus({ orderId: orderId, bankOrderId: bankOrderId }))
    }, [])

    useEffect(() => {
        if (orderPaymentStatus === 'successful') {
            dispatch(emptyCart())
            navigate('/orders', {
                state: {
                    orderId: orderId,
                    paymentStatus: orderPaymentStatus
                }
            })
        }
        else if (orderPaymentStatus === 'failure')
            navigate('/cart', {
                state: {
                    orderId: orderId,
                    paymentStatus: orderPaymentStatus
                }
            })
    }, [orderPaymentStatus])

    return createPortal(<Loader />, document.body)
}