function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
  
  async function stamp() {
    document.getElementById("stamp1").innerHTML = "Process started...";
    await sleep(30000);
    document.getElementById("stamp2").innerHTML = "...we're going, please hold. 30sec elapsed.";
    await sleep(30000);
    document.getElementById("stamp3").innerHTML = "...script running. 1 min elapsed.";
    await sleep(30000);
    document.getElementById("stamp4").innerHTML = "...script running. 1,5 min elapsed.";
  
    // Sleep in loop
    /* for (let i = 0; i < 5; i++) {
      if (i === 3)
        await sleep(2000);
      console.log(i);
    } */
  }
  
 