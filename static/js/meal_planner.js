/**
 * DIP Diet RAG Agent — Meal Planner JavaScript
 */

(function () {
  'use strict';

  const generateBtn   = document.getElementById('generatePlanBtn');
  const planContent   = document.getElementById('planContent');
  const planLoading   = document.getElementById('planLoading');
  const planEmptyState = document.getElementById('planEmptyState');
  const planSources   = document.getElementById('planSources');
  const planSourcesList = document.getElementById('planSourcesList');
  const planModelUsed = document.getElementById('planModelUsed');
  const planOutputTitle = document.getElementById('planOutputTitle');
  const copyPlanBtn   = document.getElementById('copyPlanBtn');
  const printPlanBtn  = document.getElementById('printPlanBtn');

  // Configure marked
  if (typeof marked !== 'undefined') {
    marked.setOptions({ breaks: true, gfm: true });
  }

  function getPlanType() {
    return document.querySelector('input[name="planType"]:checked')?.value || 'daily';
  }
  function getCondition() {
    return document.getElementById('conditionSelect')?.value || 'general';
  }

  function generatePlan(planType, condition) {
    const conditionLabels = {
      general:     '🌿 General Wellness',
      diabetes:    '🩺 Diabetes-Friendly',
      weight_loss: '⚖️ Weight Loss',
      heart:       '❤️ Heart Health',
      pcos:        '👩‍⚕️ PCOS Support',
    };
    const typeLabel = planType === 'weekly' ? 'Weekly' : 'Daily';
    planOutputTitle.textContent = `${typeLabel} ${conditionLabels[condition] || 'DIP Diet'} Plan`;

    planEmptyState.classList.add('d-none');
    planLoading.classList.remove('d-none');
    planContent.classList.add('d-none');
    planSources.classList.add('d-none');
    planModelUsed.classList.add('d-none');
    copyPlanBtn.classList.add('d-none');
    printPlanBtn.classList.add('d-none');

    fetch('/api/meal-plan/generate', {
      method:  'POST',
      headers: { 'Content-Type': 'application/json' },
      body:    JSON.stringify({ plan_type: planType, condition })
    })
    .then(r => r.json())
    .then(data => {
      planLoading.classList.add('d-none');
      if (data.error) {
        planContent.innerHTML = `<div class="alert alert-danger">${data.error}</div>`;
      } else {
        planContent.innerHTML = typeof marked !== 'undefined'
          ? marked.parse(data.content || '')
          : (data.content || '').replace(/\n/g, '<br/>');
      }
      planContent.classList.remove('d-none');

      if (data.sources && data.sources.length) {
        planSourcesList.innerHTML = data.sources.slice(0, 4).map(s =>
          `<span class="badge bg-light text-muted border me-1 mb-1">
             <i class="bi bi-book me-1"></i>${s.source} — ${s.section}
           </span>`
        ).join('');
        planSources.classList.remove('d-none');
      }
      if (data.model_used) {
        planModelUsed.innerHTML = `<i class="bi bi-cpu me-1"></i>${data.model_used}`;
        planModelUsed.classList.remove('d-none');
      }
      copyPlanBtn.classList.remove('d-none');
      printPlanBtn.classList.remove('d-none');
    })
    .catch(() => {
      planLoading.classList.add('d-none');
      planContent.innerHTML = '<div class="alert alert-warning">Could not generate meal plan. Please try again.</div>';
      planContent.classList.remove('d-none');
    });
  }

  // Main generate button
  if (generateBtn) {
    generateBtn.addEventListener('click', () => {
      generatePlan(getPlanType(), getCondition());
    });
  }

  // Sample plan quick-load buttons
  document.querySelectorAll('.sample-plan-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const condition = btn.dataset.condition;
      const planType  = btn.dataset.type;
      // Sync controls
      const radioId = planType === 'weekly' ? 'planWeekly' : 'planDaily';
      const radio = document.getElementById(radioId);
      if (radio) radio.click();
      const condSelect = document.getElementById('conditionSelect');
      if (condSelect) condSelect.value = condition;
      generatePlan(planType, condition);
    });
  });

  // Copy plan
  if (copyPlanBtn) {
    copyPlanBtn.addEventListener('click', () => {
      const text = planContent.innerText || planContent.textContent;
      navigator.clipboard.writeText(text).then(() => {
        copyPlanBtn.innerHTML = '<i class="bi bi-check me-1"></i>Copied!';
        setTimeout(() => {
          copyPlanBtn.innerHTML = '<i class="bi bi-clipboard me-1"></i>Copy';
        }, 2000);
      });
    });
  }

  // Print plan
  if (printPlanBtn) {
    printPlanBtn.addEventListener('click', () => window.print());
  }

})();
