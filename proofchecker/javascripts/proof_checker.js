/**
 * A JavaScript file containing code that manipulates the behavior of the various form elements on the Validate Your Proof page
 */


//Add Line button
const addMoreBtn = document.getElementById("add-more")
const totalNewForms = document.getElementById("id_form-TOTAL_FORMS")
const currentProofLineForms = document.getElementsByClassName("proofline-form")
addMoreBtn.addEventListener("click", add_new_form)

function add_new_form(event){
    if (event){
        event.preventDefault()
    }
    let currentFormCount = currentProofLineForms.length
    const formCopyTarget = document.getElementById("proof-line-list")
    const emptyFormElement = document.getElementById("empty-form").cloneNode(true)
    emptyFormElement.setAttribute("class", "proofline-form")
    emptyFormElement.setAttribute("id", `form-${currentFormCount}`)
    const regex = new RegExp('__prefix__', 'g')
    emptyFormElement.innerHTML = emptyFormElement.innerHTML.replace(regex, currentFormCount)
    totalNewForms.setAttribute('value', currentFormCount + 1)
    formCopyTarget.append(emptyFormElement)
}

//Add symbol replacement functionality to input fields
const inputFields = document.getElementsByClassName("text-replacement-enabled")

for (let i of inputFields){
    console.log(i)
    i.setAttribute("onkeydown", "replaceCharacter(this);")
}