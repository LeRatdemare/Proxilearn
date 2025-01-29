// Ici on a accès à la variable answerType qui contient le type de réponse attendu
const coin = document.querySelectorAll('.coin');
const sortedListElement = document.getElementById('sorted-list');
const selectedValuesInput = document.getElementById('inputText');
let selectedValues = [];

coin.forEach(coin => {
  coin.addEventListener('click', () => {
    // Récupérer la valeur associée à l'image
    const value = parseFloat(coin.getAttribute('data-value'));

    if (answerType === 'I' || answerType === 'T') {
      clearInput();
    }
    // Ajouter la valeur à la liste
    selectedValues.push(value);

    // Trier la liste par ordre croissant
    selectedValues.sort((a, b) => b - a);

    // Afficher la liste triée
    sortedListElement.textContent = selectedValues.join(', ');

    selectedValuesInput.value = selectedValues.join(',');
  });
});

function clearInput() {
  selectedValues = [];
  sortedListElement.textContent = '';
  selectedValuesInput.value = '';
}