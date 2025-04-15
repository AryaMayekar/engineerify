const question = document.getElementById("question");
const choices = Array.from(document.getElementsByClassName("choice-text"));
const nextButton = document.getElementById("nextbtn");
const prevButton = document.getElementById("prevbtn");
const submitButton = document.getElementById("submitbtn");
const container = document.getElementById("container");
const finalmarks_container = document.getElementById("finalmarks-container");
const finalMessage = document.getElementById('final-message');
const finalMessage2 = document.getElementById('final-message2');

let userAnswers = [null, null, null, null, null]; // Initialize with null


let currentQuestion = {};
let questionCounter = 0;
let availableQuestions = [];
let questionIndex = 0;// Always pick the first question from the array
let totalTime = 60; // Total time in seconds (1 minute)
let timeLeft = totalTime; // Time remaining
let timerInterval; // To hold the timer interval
//constants
const MAX_QUESTIONS = 4;


//available questions
let questions = [
  {
    question: "Q.1  What is the speed of light in vacuum?",
    choice1: "3 × 10⁸ m/s",
    choice2: "3 × 10⁶ m/s",
    choice3: "3 × 10⁵ km/h",
    choice4: "3 × 10⁷ m/s",
    answer: 1,
  },
  {
    question: "Q.2  Which element has the lowest ionization energy?",
    choice1: "Oxygen",
    choice2: "Sodium",
    choice3: "Chlorine",
    choice4: "Fluorine",
    answer: 2,
  },
  {
    question: "Q.3  If f(x) = x² + 3x + 2, what is f(2)?",
    choice1: "10",
    choice2: "12",
    choice3: "8",
    choice4: "16",
    answer: 1,
  },
  {
    question: "Q.4  Which of the following is the odd one out in logical reasoning?",
    choice1: "Apple",
    choice2: "Banana",
    choice3: "Carrot",
    choice4: "Mango",
    answer: 3,
  },
  {
    question: "Q.5  Which gas is used in fluorescent lamps?",
    choice1: "Oxygen",
    choice2: "Argon",
    choice3: "Nitrogen",
    choice4: "Helium",
    answer: 2,
  },
];



//starts the quiz
startgame = () => {
    questionCounter = 0;
    availableQuestions = [...questions];
    startTimer();
    loadQuestion(questionIndex);
};

//loads a question 
const loadQuestion = (index) => {
    
    currentQuestion = availableQuestions[index];
    question.innerText = currentQuestion.question;
    
    console.log(`Stored answers: ${userAnswers}`);
  
    choices.forEach((choice) => {
      const number = choice.dataset["number"];
      choice.innerText = currentQuestion["choice" + number];
      
      // Reset background for all options to white
      choice.style.backgroundColor = "white";
      choice.style.color = "black"; 

      // If an answer was selected for this question, highlight the selected option
    if (userAnswers[index] == number) {
        choice.style.backgroundColor = "#a0d3ff"; // Highlight selected option
        choice.style.color = "black"; // Keep text color readable
      }
      
    });
    // Hide or show buttons based on the current question index
    updateQuestionNumber();
  toggleButtons();
  };

  //timer
const startTimer = () => {
  timerInterval = setInterval(() => {
    if (timeLeft > 0) {
      timeLeft--;
      const minutes = Math.floor(timeLeft / 60);
      const seconds = timeLeft % 60;
      document.getElementById("timer").textContent = `${minutes}:${seconds < 10 ? '0' : ''}${seconds}`;
    } else {
      clearInterval(timerInterval);
      calculateScore(); // Automatically calculate score when time runs out
    }
  }, 1000);
};

// Update question number (e.g., 1/5)
const updateQuestionNumber = () => {
  const questionNumberElement = document.getElementById("question-number");
  questionNumberElement.textContent = `${questionIndex + 1}/5`;
};
  
  choices.forEach((choice) => {
    choice.addEventListener("click", () => {
      
  
      const selectedOption = parseInt(choice.dataset["number"]); // Convert to integer
      userAnswers[questionIndex] = selectedOption; // Store the selected option
      
      // Immediately change the color of the selected choice
    choice.style.backgroundColor = "#a0d3ff"; // Highlight selected option
    choice.style.color = "white"; // Ensure the text color is readable

      // Reset all options to white and only color the selected one
      choices.forEach((c) => {
        if (c !== choice){
        c.style.backgroundColor = "white";
        c.style.color = "black";
       }
      });
    });
  })
  
  const toggleButtons = () => {
    // Show/Hide Prev button
    if (questionIndex === 0) {
      prevButton.style.display = "none"; // Hide Prev button if it's the first question
    } else {
      prevButton.style.display = "inline-block"; // Show Prev button otherwise
    }
  
    // Show/Hide Next button and Submit button
    if (questionIndex === availableQuestions.length - 1) {
      nextButton.style.display = "none"; // Hide Next button if it's the last question
      submitButton.style.display = "inline-block"; // Show Submit button if it's the last question
    } else {
      nextButton.style.display = "inline-block"; // Show Next button if not the last question
      submitButton.style.display = "none"; // Hide Submit button otherwise
    }
  };

  nextButton.addEventListener("click", () => {
    if (questionIndex < MAX_QUESTIONS) {
      ++questionIndex;
      loadQuestion(questionIndex);
    } 
  });
  
  prevButton.addEventListener("click", () => {
    if (questionIndex > 0) {
      questionIndex--;
      loadQuestion(questionIndex);
    } 
  });

  function askUser() {
    const modal = document.getElementById("submit-modal");
    const remainingQuestionsSpan = document.getElementById("remaining-questions");
    const mainContent = document.getElementById("container");
  
    // 1. Show the badadiv
    modal.style.display = "flex";
    modal.style.justifyContent = "center";
    modal.style.alignItems = "center";
  
    // 2. Blur the background
    mainContent.classList.add("blurred");
    modal.style.filter = "none";
  
    // 3. Calculate remaining time in MM:SS format
    const updateModalContent = () => {
      const minutes = Math.floor(timeLeft / 60);
      const seconds = timeLeft % 60;
      const formattedTime = `${minutes}:${seconds < 10 ? '0' : ''}${seconds}`;
      document.getElementById("remaining-time").textContent = formattedTime;
  
      // Count nulls in userAnswers
      const unattempted = userAnswers.filter(answer => answer === null).length;
      document.getElementById("remaining-questions").textContent = unattempted;
    };
    // Update once immediately
    updateModalContent();

    // Start updating modal content every second
    modalInterval = setInterval(updateModalContent, 1000);
  
    // 4. Count how many questions are unattempted (null values)
    const unattemptedCount = userAnswers.filter(ans => ans === null).length;
    remainingQuestionsSpan.innerText = unattemptedCount;
}

submitButton.addEventListener("click", () => {
  askUser(); // Show confirmation modal instead of direct submit
});

// Function to close the modal and remove the blur effect
const notNow = () => {
  // Hide the modal
  const modal = document.getElementById('submit-modal');
  modal.style.display = 'none'; // Hides the modal

  // Remove the blur effect from the background
  container.classList.remove('blurred');
};

// Add an event listener to the "Not Now" button
document.getElementById('cancel-submit').addEventListener('click', notNow);

  const calculateScore = () => {
    let score = 0;
  
    questions.forEach((question, index) => {
      const userAnswer = userAnswers[index];
    
      if (userAnswer === null) {
        score += 0; // Unattempted
      } else if (userAnswer === question.answer) {
        score += 3; // Correct answer
      } else {
        score -= 1; // Incorrect answer
      }
    });
  
    // Display the score
    
    showFinalMessage(score);
    
  };

  // Function for confirm-submit button to calculate score and close the modal
  const confirmSubmit = () => {
    calculateScore(); // Call calculateScore when the submit button is clicked
  };

  // Add an event listener to the "Submit Test" button
document.getElementById('confirm-submit').addEventListener('click', confirmSubmit);

// Function to display the final message based on the score
const showFinalMessage = (scoredisplay) => {
    
    // Display the final marks container
    const modal = document.getElementById('submit-modal');
    modal.style.display = 'none'; // Hides the modal
    container.style.display = "none"; // Hide the quiz section
    finalmarks_container.style.display = "inline-block"; // display the result section

   // Set the message based on the score
    if (scoredisplay >= 15) {
      finalMessage.innerHTML = `Great job! You've completed the quiz.`;
      finalMessage2.innerHTML =` Your score is ${scoredisplay}. Keep it up!`;
    } else if (scoredisplay >= 10) {
      finalMessage.innerHTML = `Good effort! Your score is ${scoredisplay}.`;
      finalMessage2.innerHTML =`Don't worry, keep practicing!`;
    } else{
      finalMessage.innerHTML = `Oops! Your score is ${scoredisplay}.`;
      finalMessage2.innerHTML = `Try again for a higher score!`;
    }
    senddata(scoredisplay);
    
  };

 //sending data to backend
const senddata = (storescore) => {
  
  const stscore = storescore;
  
  fetch('/save_score_bitsat',{
    method: 'POST',
    headers:{
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ intValue: stscore}),
  })
  .then(response => response.json())
  .then(response => {console.log('Server response:', response);})
  .catch(error => {console.error('Error:', error);});
}

startgame();