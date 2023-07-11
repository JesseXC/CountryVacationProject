let tabs = document.querySelector(".tabs");
let tabHeader = tabs.querySelector(".tab-header");
let tabHeaderNodes = tabs.querySelectorAll(".tab-header > div");
let tabContent = tabs.querySelector(".tab-content");
let tabContentNodes = tabs.querySelectorAll(".tab-content > div");

for (let i = 0; i < tabHeaderNodes.length; i++) {
  tabHeaderNodes[i].addEventListener("click", function() {
    tabHeader.querySelector(".active").classList.remove("active");
    tabHeaderNodes[i].classList.add("active");
    tabContent.querySelector(".active").classList.remove("active");
    tabContentNodes[i].classList.add("active");
  });
}

console.log("JavaScript code executed!");
