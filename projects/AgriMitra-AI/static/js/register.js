const originalTexts={
imageText:"Smart Farming • Better Decisions • Better Future",
title:"Create Your Account",
subtitle:"Join AgriMitra AI and make smarter farming decisions.",
name:"Full Name",
namePlaceholder:"Enter your full name",
userid:"User ID",
useridPlaceholder:"Create a user ID",
email:"Email",
emailPlaceholder:"Enter your email",
phone:"Phone Number",
phonePlaceholder:"Enter your phone number",
password:"Password",
passwordPlaceholder:"Create a password",
confirm:"Confirm Password",
confirmPlaceholder:"Confirm your password",
language:"Preferred Language",
button:"Create Account",
already:"Already have an account?",
login:"Login"
};

const registeredElements=[
["imageText",originalTexts.imageText],
["registerTitle",originalTexts.title],
["registerSubtitle",originalTexts.subtitle],
["nameLabel",originalTexts.name],
["useridLabel",originalTexts.userid],
["emailLabel",originalTexts.email],
["phoneLabel",originalTexts.phone],
["passwordLabel",originalTexts.password],
["confirmLabel",originalTexts.confirm],
["preferredLanguageLabel",originalTexts.language],
["alreadyAccount",originalTexts.already],
["loginLink",originalTexts.login]
];

const placeholderTargets=[
["fullname",originalTexts.namePlaceholder],
["userid",originalTexts.useridPlaceholder],
["email",originalTexts.emailPlaceholder],
["phone",originalTexts.phonePlaceholder],
["password",originalTexts.passwordPlaceholder],
["confirmPassword",originalTexts.confirmPlaceholder]
];

async function translateTexts(texts,language){
if(language==="en")return texts;
try{
const response=await fetch("/translate",{
method:"POST",
headers:{"Content-Type":"application/json"},
body:JSON.stringify({texts:texts,language:language})
});
if(!response.ok)throw new Error("Translation failed");
const data=await response.json();
return (data.translations&&data.translations.length===texts.length)?data.translations:texts;
}catch(error){
console.error("Translation error:",error);
return texts;
}
}

async function updateLanguage(language){
const allTexts=registeredElements.map(function(e){return e[1];})
.concat(placeholderElements.map(function(e){return e[1];}))
.concat([originalTexts.button]);
const translated=await translateTexts(allTexts,language);

registeredElements.forEach(function(entry,i){
const element=document.getElementById(entry[0]);
if(element)element.textContent=translated[i];
});

placeholderElements.forEach(function(entry,i){
const element=document.getElementById(entry[0]);
if(element)element.placeholder=translated[registeredElements.length+i];
});

const button=document.querySelector("#registerButton span");
if(button)button.textContent=translated[allTexts.length-1];
}

document.getElementById("language").addEventListener("change",async function(){
const language=this.value;
document.getElementById("preferredLanguage").value=language;
await updateLanguage(language);
});

document.getElementById("preferredLanguage").addEventListener("change",async function(){
const language=this.value;
document.getElementById("language").value=language;
await updateLanguage(language);
});

document.getElementById("registerForm").addEventListener("submit",async function(e){
e.preventDefault();

const fullname=document.getElementById("fullname").value.trim();
const userid=document.getElementById("userid").value.trim();
const email=document.getElementById("email").value.trim();
const phone=document.getElementById("phone").value.trim();
const password=document.getElementById("password").value;
const confirmPassword=document.getElementById("confirmPassword").value;
const language=document.getElementById("preferredLanguage").value;
const message=document.getElementById("message");

if(!fullname||!userid||!email||!password){
message.textContent="Please fill all required fields.";
message.style.color="red";
return;
}

if(password.length<6){
message.textContent="Password must contain at least 6 characters.";
message.style.color="red";
return;
}

if(password!==confirmPassword){
message.textContent="Passwords do not match.";
message.style.color="red";
return;
}

try{
const response=await fetch("/register",{
method:"POST",
headers:{"Content-Type":"application/json"},
body:JSON.stringify({
fullname:fullname,
userid:userid,
email:email,
phone:phone,
password:password,
language:language
})
});

const data=await response.json();

if(data.success){
message.textContent=data.message;
message.style.color="green";

setTimeout(function(){
window.location.href="/login";
},1500);
}else{
message.textContent=data.message;
message.style.color="red";
}

}catch(error){
console.error(error);
message.textContent="Unable to connect to server.";
message.style.color="red";
}
});

function togglePassword(id,icon){
const input=document.getElementById(id);

if(input.type==="password"){
input.type="text";
icon.classList.remove("fa-eye");
icon.classList.add("fa-eye-slash");
}else{
input.type="password";
icon.classList.remove("fa-eye-slash");
icon.classList.add("fa-eye");
}
}

updateLanguage("en");