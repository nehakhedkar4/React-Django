import React, {useEffect,useState} from 'react'
import axios from 'axios'

const RazorPayPayment = () => {
    const [orderID, setOrderID] = useState(null);

//   const loadScript = (src) => {  
//     console.log("*********loaded")
//     return new Promise((resolve) => {
//       const script = document.createElement("script");
//       script.src = src;
//       script.onload = () => {
//         resolve(true);
//       };
//       script.onerror = () => {
//         resolve(false);
//       };
//     document.body.appendChild(script);
//   });
// };

// useEffect(() => {
//     loadScript("https://checkout.razorpay.com/v1/checkout.js");
// });

    useEffect(() => {
        const script = document.createElement('script');
        script.src = 'https://checkout.razorpay.com/v1/checkout.js';
        script.async = true;
        document.body.appendChild(script);
      }, []);

      const initiatePayment = async (e) => {
        e.preventDefault();
        try {
          const response = await axios.post( "http://127.0.0.1:8000/razorpay/" );
          console.log("response", response.data.payment);
          setOrderID(response.data.payment.id)
        } catch (error) {
          console.log(error);
        }
      }

      var options = {
        "key_id": "rzp_test_mQX5zJOEMTb076", // Enter the Key ID generated from the Dashboard
        "key_secret": "QZoWctpequlkR9MeUUrWOuW9",
        "amount": 1*100, // Amount is in currency subunits. Default currency is INR. Hence, 50000 refers to 50000 paise
        "currency": "INR",
        "name": "Acme Corp", //your business name
        "description": "Test Transaction",
        "image": "https://example.com/your_logo",
        "order_id": orderID, //This is a sample Order ID. Pass the `id` obtained in the response of Step 1
        "handler": function (response){
          alert(response.razorpay_payment_id);
          // alert(response.razorpay_order_id);
          // alert(response.razorpay_signature)
      },
        "prefill": {
            "name": "Gaurav Kumar", //your customer's name
            "email": "gaurav.kumar@example.com",
            "contact": "9000090000"
        },
        "notes": {
            "address": "Razorpay Corporate Office"
        },
        "theme": {
            "color": "#3399cc"
        }
      };
    
        const rzp1 = new window.Razorpay(options);
        rzp1.open();
      
    
  return (
    <>
        <div>RazorPayPayment
            <button onClick={initiatePayment} >Pay</button>
        </div>
    </>
  )
}

export default RazorPayPayment