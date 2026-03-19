import { createContext, useContext, useState, useEffect } from "react";
import { HOSTNAME } from "./conf.js";


const UserContext = createContext(null)
const ProductsContext = createContext([])
const ProductContext = createContext(null)
const OrderPaymentStatusContext = createContext(null)

export const useUser = () => useContext(UserContext)
export const useProducts = () => useContext(ProductsContext)
export const useProduct = () => useContext(ProductContext)
export const useOrderPaymentStatus = () => useContext(OrderPaymentStatusContext)

export const UserProvider = ({children}) => {
    const [user, setUser] = useState(null)
    const [loading, setLoading] = useState(true)

    async function fetchUserData() {
        setLoading(true)

        try {
            const response = await fetch(`${HOSTNAME}/api/user/`, {
                credentials: 'include',
                method: 'GET'
            })

            if (response.status !== 200) {
                setLoading(false)
                return
            }

            const {id, first_name, username, image, cart, orders} = await response.json()
            setUser({
                id: id,
                name: first_name,
                username: username,
                image: image,
                cart: cart,
                orders: orders.toReversed()
            })
            console.log(user)
        }
        catch (e) {
            console.log('fetchUserData error:', e)
            setUser(null)
        }
        finally {
            setLoading(false)
        }
    }

    useEffect(() => {fetchUserData()}, [location.pathname, location.search])

    async function refreshUser() {
        fetchUserData()
    }

    return (
        <UserContext.Provider value = {{user, setUser, loading, refreshUser}}>
            {children}
        </UserContext.Provider>
    )
}

export const ProductsProvider = ({type, name, priceMin, priceMax, children}) => {
    const [products, setProducts] = useState([])
    const [loading, setLoading] = useState(true)
    const url = new URL(`${HOSTNAME}/api/products/`)

    if (type) url.searchParams.append('type', type)
    if (name) url.searchParams.append('name', name)
    if (priceMin) url.searchParams.append('price_min', priceMin)
    if (priceMax) url.searchParams.append('price_max', priceMax)

    async function fetchProducts() {
        setLoading(true)

        try {
            const response = await fetch(url)
            const data = await response.json()
            setProducts(data)
        }
        catch (e) {
            console.log('fetchProducts error:', e)
            setProducts([])
        }
        finally {
            setLoading(false)
        }
    }

    useEffect(() => {fetchProducts()}, [location.pathname, location.search])

    return (
        <ProductsContext.Provider value = {{products, setProducts, loading}}>
            {children}
        </ProductsContext.Provider>
    )
}

export const ProductProvider = ({productUUID, children}) => {
    const [product, setProduct] = useState(null)
    const [loading, setLoading] = useState(true)

    async function fetchProduct() {
        setLoading(true)

        try {
            const response = await fetch(`${HOSTNAME}/api/products/${productUUID}/`)
            const {id, type, name, price, description, images} = await response.json()
            setProduct({
                id: id,
                type: type,
                name: name,
                price: price,
                description: description,
                images: images
            })
        }
        catch (e) {
            console.log('Error while fetching product:', e)
            setProduct(null)
        }
        finally {
            setLoading(false)
        }
    }

    useEffect(() => {fetchProduct()}, [location.pathname, location.search])

    return (
        <ProductContext.Provider value = {{product, setProduct, loading}}>
            {children}
        </ProductContext.Provider>
    )
}

export const OrderPaymentStatusProvider = ({orderId, bankOrderId, children}) => {
    const [paymentStatus, setPaymentStatus] = useState(null)
    const [loading, setLoading] = useState(true)

    async function fetchOrderPaymentStatus() {
        setLoading(true)

        try {
            const response = await fetch(`${HOSTNAME}/api/orders/${orderId}/payment/check/?bankOrderId=${bankOrderId}`, {
                credentials: 'include'
            })
            const {paymentStatus} = await response.json() // Статусы оплаты: successful, failure
            setPaymentStatus(paymentStatus)
        }
        catch (e) {
            console.log('Error whole fetching product payment status:', e)
            setPaymentStatus(null)
        }
        finally {
            setLoading(false)
        }
    }

    useEffect(() => {fetchOrderPaymentStatus()}, [orderId, bankOrderId])

    return (
        <OrderPaymentStatusContext.Provider value = {{orderId, paymentStatus, loading}}>
            {children}
        </OrderPaymentStatusContext.Provider>
    )
}