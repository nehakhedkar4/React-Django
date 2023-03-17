import React from 'react'

const StripePayment = () => {
  return (
    <div>Payment
        <form action={'http://127.0.01:8000/payment/'} method="post">
            <button type='submit'>Pay Now</button>
        </form>
    </div>
  )
}

export default StripePayment