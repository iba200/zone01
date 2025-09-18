const mousemouve = document.getElementById('mousemove')
console.log(mousemouve)
window.addEventListener("mousemove", (e) => {
    mousemouve.style.left = e.pageX + "px"
    mousemouve.style.top = e.pageY + "px"
})
window.addEventListener("click", (e) => {
    mousemouve.classList.toggle("active")

})

const name = document.getElementById('name')
const email = document.getElementById('email')
const form = document.getElementById('form')
const number = document.getElementById('number')
const errorElement = document.getElementById('error')

function emailIsValid (email) {
  return /\S+@\S+\.\S+/.test(email)
}



form.addEventListener('submit', (e) => {
    let messages = []
    if (name.value === '' || name.value == null){
        messages.push('Name is required')
    }

    if (email.value != '' & emailIsValid(email.value) === false){
        messages.push('Email is not valid')
    }
    if (email.value === '' || email.value == null){
        messages.push('Email is required')
    }
    if (number.value === '' || number.value == null){
        messages.push('Number is required')
    }
    if (messages.length > 0){
        e.preventDefault()
        errorElement.innerText = messages.join(', ')
        errorElement.style.color = 'red'
        errorElement.style.fontSize = '20'+'px'
    }

})
