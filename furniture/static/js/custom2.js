


const overlay = document.getElementById("offer-loader");
  const closeOverlay = document.getElementById("close-modal");
  closeOverlay.addEventListener('click', (event) => {
    overlay.style.display = 'none';
  })
  overlay.addEventListener('click', (event) => {
    if (event.target === overlay) {
      overlay.style.display = 'none';
    }
  })
  document.addEventListener("DOMContentLoaded", function () {
    if (!sessionStorage.getItem("overlay_displayed")) {
      overlay.style.display = 'flex';
      sessionStorage.setItem("overlay_displayed", "true");
    }
  })
  var input = document.getElementById("pincodeInput");
  // Execute a function when the user presses a key on the keyboard
  input.addEventListener("keypress", function (event) {
    // If the user presses the "Enter" key on the keyboard
    if (event.key === "Enter") {
      // Cancel the default action, if needed
      event.preventDefault();
      // Trigger the button element with a click
      document.getElementById("pincodeClick").click();
    }
  });
  function checkDelivery() {
    const pincode = document.getElementById("pincodeInput").value;
    const result = document.getElementById("text-para");
    const result2 = document.getElementById("text-para2");
    const now = new Date();
    const istDate = new Date(now.toLocaleString("en-US", { timeZone: "Asia/Kolkata" }));
    const days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
    const months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
    let today = new Date();
    fetch(`https://api.postalpincode.in/pincode/${pincode}`)
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })

      .then(data => {
        if (data[0].Status == "Success") {
          const locarray = ["Thrissur", "Alappuzha", "Ernakulam"]
          const location = data[0]["PostOffice"];
          result.setAttribute('style', 'font-weight:bold')
          for (let index = 0; index < location.length; index++) {
            if (locarray.includes(location[index].District)) {
              if ((today.getDate() + 2) > (getDaysInMonth(today.getFullYear(), today.getMonth()))) {
                let month = today.getMonth();
                const newDate = (today.getDate() + 2) - (getDaysInMonth(today.getFullYear(), today.getMonth() + 1));
                today.setDate(newDate);
                today.setMonth(month + 1);
                result.innerText = `FREE delivery by ${days[today.getDay()]}, ${today.getDate()} ${months[today.getMonth()]} `;
                result2.innerText = `Deliver to ${location[index].Division},${location[index].District} ${pincode} `;
              } else {
                result.innerText = `FREE delivery by ${days[today.getDay() + 2]}, ${today.getDate() + 2} ${months[today.getMonth()]} `;
                result2.innerText = `Deliver to ${location[index].Block},${location[index].District} ${pincode} `;
              }
              break;
            } else {
              /*if ((today.getDate() + 7) > (getDaysInMonth(today.getFullYear(), today.getMonth()))) {
                let month = today.getMonth();
                const newDate = (today.getDate() + 7) - (getDaysInMonth(today.getFullYear(), today.getMonth() + 1));
                today.setDate(newDate);
                today.setMonth(month + 1);
                result.innerText = `FREE delivery by ${days[today.getDay()]}, ${today.getDate()} ${months[today.getMonth()]} `;
                result2.innerText = `Deliver to ${location[index].Block},${location[index].District} ${pincode} `;
              } else {
                result.innerText = `FREE delivery by ${days[today.getDay() + 7]}, ${istDate.getDate() + 7} ${months[today.getMonth()]} `;
                result2.innerText = `Deliver to ${location[index].Block},${location[index].District} ${pincode} `;
              }*/
             result.innerText = `We don't ship to this pincode currently`;
             result2.innerText = ``;
              break;
            }
          }
        } else {
          result.setAttribute('style', 'font-weight:bold');
          result.innerText = "Please enter a valid pincode";
          result2.innerText = "";
        }

      })
      .catch(error => console.error('There was a problem with the fetch operation:', error));

  }

  function getDaysInMonth(year, month) {
    return new Date(year, month, 0).getDate();
  }
  const mainImage = document.getElementById("mainImage");

  const qtyInput = document.getElementById("qtyInput");
  const url = document.getElementById("addtocart");
  const url2 = document.getElementById("buynow");
  const url3 = document.getElementById("addtowishlist");
  let qtyValue = qtyInput.value;
  const totalPriceEl = document.getElementById("totalPrice");
  const pricePerUnit = parseInt(document.getElementById("totalPrice").textContent.replace(",", ""));
  const productId = "{{ product.id }}";

  

  function adjustQty(val, productId) {
    let qty = parseInt(qtyInput.value);
    qty = isNaN(qty) ? 1 : qty;
    qty = Math.max(1, qty + val);
    qtyInput.value = qty;
    qtyValue = qty;
    qtyInput.setAttribute("value", `${qtyValue}`)
    url2.setAttribute("href", `/buy/${productId}/${qtyValue}/`);
    url3.setAttribute("href", `/add/wishlist/${productId}/${qtyValue}/`);
    totalPriceEl.textContent = qty * pricePerUnit;
  }

  qtyInput.addEventListener("input", () => {
    let qty = parseInt(qtyInput.value);
    qty = isNaN(qty) || qty < 1 ? 1 : qty;
    qtyInput.value = qty;
    totalPriceEl.textContent = qty * pricePerUnit;
  });


  const stars = document.querySelectorAll('.star');
    const ratingInput = document.getElementById('rating');
    let selectedRating = 0;

    stars.forEach(star => {
        star.addEventListener('mouseover', () => {
            highlightStars(star.dataset.value);
        });

        star.addEventListener('mouseout', () => {
            highlightStars(selectedRating);
        });

        star.addEventListener('click', () => {
            selectedRating = star.dataset.value;
            ratingInput.value = selectedRating;
            highlightStars(selectedRating);
        });
    });

    function highlightStars(rating) {
        stars.forEach(star => {
            if (star.dataset.value <= rating) {
                star.classList.add('selected');
            } else {
                star.classList.remove('selected');
            }
        });
    }
    const imageInput = document.getElementById('img');
    const preview = document.getElementById('preview');

    imageInput.addEventListener('change', function(event) {
      const file = event.target.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
          preview.src = e.target.result;
          preview.style.display = 'block';
        };
        reader.readAsDataURL(file);
      }
    });

    function getWishStatus(product_id) {
    const like_icon = document.getElementById(`cart-like${product_id}`);
    if (like_icon.getAttribute("fill") == "none") {
      console.log(like_icon.getAttribute("fill"));
      const url = `/add/wishlist/${product_id}/1/`;
      console.log(url);
      like_icon.setAttribute("fill","red");
      return url;
    } else if(like_icon.getAttribute("fill") == "red") {
      const url = `/remove/wishlist/${product_id}/`;
      like_icon.setAttribute("fill","none");
      console.log(url);
      return url;
    }
  }

  function addToWishlist(product_id) {
    const url = getWishStatus(product_id)
    fetch(url, {
      headers: {
        "X-Requested-With": "XMLHttpRequest"
      }
    })
      .then(response => response.text())
      .then(html => {
        document.getElementById("scroll-products").innerHTML = html;
      })

  }

