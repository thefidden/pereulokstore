import React, { useEffect } from "react";
import { createPortal } from "react-dom";
import { useNavigate } from "react-router-dom";

import Loader from "../components/loader.jsx";
import { useOrderPaymentStatus, useUser } from "../ContextProviders.jsx";
import { deleteOrder, emptyUserCart } from "../utils.js";


const OrderCheckPaymentPage = () => {
    const navigate = useNavigate()
    const {user} = useUser()
    const {orderId, paymentStatus, loading} = useOrderPaymentStatus()

    useEffect(() => {
        const proceedOrder = async () => {
            if (paymentStatus === 'successful') {
                await emptyUserCart()
                navigate('/orders', {
                    state: {
                        orderId: orderId,
                        paymentStatus: paymentStatus
                    }
                })
            }

            else if (paymentStatus === 'failure') {
                await deleteOrder(orderId)
                navigate('/cart', {
                    state: {
                        orderId: orderId,
                        paymentStatus: paymentStatus
                    }
                })
            }
        }
        const _ = proceedOrder()
    }, [paymentStatus]);

    return createPortal(<Loader/>, document.body)
}

export default OrderCheckPaymentPage