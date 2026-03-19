import { HOSTNAME } from "./conf.js";
import { useNavigate } from "react-router-dom";


export const getCookie = (name) => {
    let cookieValue = null

    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';')

        for (let cookie of cookies) {
            cookie = cookie.trim();

            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break
            }
        }
    }

    return cookieValue
}

export const userHasProductInCart = (user, product) => {
    return (user == null || product == null) ? false
                                             : user.cart.map(cartItem => cartItem.product.id).includes(product.id)
}

export const addProductToCart = async (product) => {
    const response = await fetch(`${HOSTNAME}/api/carts/`, {
        method: 'POST',
        credentials: 'include',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({
            'productId': product.id
        })
    })
}

export const updateCartItem = async (cartItem, amount, user, setUser) => {
    const response = await fetch(`${HOSTNAME}/api/carts/${cartItem.id}/`, {
        method: 'PATCH',
        credentials: 'include',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({
            'amount': amount
        })
    })
    const newItem = await response.json()

    if (amount === 0)
        await deleteCartItem(cartItem)
}

export const deleteCartItem = async (cartItem) => {
    const response = await fetch(`${HOSTNAME}/api/carts/${cartItem.id}/`, {
        method: 'DELETE',
        credentials: 'include',
        headers: {'X-CSRFToken': getCookie('csrftoken')}
    })
}

export const deauthenticate = async (navigate) => {
    const response = await fetch(`${HOSTNAME}/api/user/deauthenticate/`, {
        method: 'GET',
        credentials: 'include'
    })
    navigate('/')
    window.location.reload()
}

export const registerOrder = async () => {
    const response = await fetch(`${HOSTNAME}/api/orders/`, {
        method: 'POST',
        credentials: 'include',
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
    const {formUrl} = await response.json()
    return window.open(formUrl, '_blank')
}

export const emptyUserCart = async () => {
    const response = await fetch(`${HOSTNAME}/api/user/empty-cart`, {
        method: 'GET',
        credentials: 'include'
    })
}

export const deleteOrder = async (orderId) => {
    const response = await fetch(`${HOSTNAME}/api/orders/${orderId}/`, {
        method: 'DELETE',
        credentials: 'include',
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
}

