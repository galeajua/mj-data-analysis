<script>
  import { onMount } from 'svelte';
  let prediction;
  let output;
  let points = '';
  let total_rebounds = '';
  let minutes_played = '';
  let field_goal_made = '';
  let three_pointers_made = '';
  let free_throws_made = '';
  let mj_career_game = '';
  let team_game_this_season = '';
  let assists = '';
  let steals = '';
  let blocks = '';
  let personal_fouls = '';

  async function predictOutcome() {
    const queryParams = new URLSearchParams({
        mj_career_game,
        team_game_this_season,
        minutes_played,
        field_goal_made,
        three_pointers_made,
        free_throws_made,
        total_rebounds,
        assists,
        steals,
        blocks,
        personal_fouls,
        points,
    }).toString();

    const response = await fetch(`/api/predict?${queryParams}`, {
        method: 'GET',
    });
    const data = await response.json();
    prediction = data.prediction;
    console.log('prediction:' + prediction)
    output = prediction == 1 ? 'Win' : "Loss";
    console.log('prediction user friendly:' + output)
}

</script>

<main>
  <h1>Basketball Game Outcome based on Michael Jordan performance</h1>
  
  <input type="number" bind:value={mj_career_game} placeholder="career game">
  <input type="number" bind:value={team_game_this_season} placeholder="team game season">
  <input type="number" bind:value={minutes_played} placeholder="minutes played">
  <input type="number" bind:value={field_goal_made} placeholder="field goal made">
  <input type="number" bind:value={three_pointers_made} placeholder="three pointers">
  <input type="number" bind:value={free_throws_made} placeholder="free throws">
  <input type="number" bind:value={total_rebounds} placeholder="Rebounds">
  <input type="number" bind:value={assists} placeholder="assists">
  <input type="number" bind:value={steals} placeholder="steals">
  <input type="number" bind:value={blocks} placeholder="blocks">
  <input type="number" bind:value={personal_fouls} placeholder="personal fouls">
  <input type="number" bind:value={points} placeholder="Points">

  <button on:click={predictOutcome}>Predict</button>
  
  {#if prediction !== undefined}
      <p>Prediction: {output}</p>
  {/if}
</main>

<style>
  
</style>
