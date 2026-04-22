import './style.css';
import { Dota2Datafeed } from 'dota2-datawrapper';

// Initialize the API using the library's GitHub source
const api = Dota2Datafeed.fromGitHub('Egezenn', 'dota2-datawrapper');

// Set branding assets from library
const favicon = document.createElement('link');
favicon.rel = 'icon';
favicon.href = Dota2Datafeed.urls.ASSET_URLS.FAVICON;
document.head.appendChild(favicon);

const logoSymbol = document.getElementById('logo-symbol');
const footerLogo = document.getElementById('footer-logo');
const lastUpdateSpan = document.getElementById('last-update');

if (logoSymbol) logoSymbol.src = Dota2Datafeed.urls.ASSET_URLS.FAVICON;
if (footerLogo) footerLogo.src = Dota2Datafeed.urls.ASSET_URLS.FAVICON;

async function updateLastUpdateDate(heroes) {
  if (heroes.length === 0) return;
  try {
    const heroShortName = heroes[0].name.replace('npc_dota_hero_', '');
    const response = await fetch(`./itembuilds/default_${heroShortName}.txt`);
    if (response.ok) {
      const vdf = await response.text();
      const match = vdf.match(/"Title"\s+"[^"]+ (\d{4}-\d{2}-\d{2})"/);
      if (match) {
        lastUpdateSpan.innerText = match[1];
      } else {
        lastUpdateSpan.innerText = 'Unknown';
      }
    }
  } catch (e) {
    lastUpdateSpan.innerText = 'Unavailable';
  }
}

const heroGrid = document.getElementById('hero-grid');
const searchInput = document.getElementById('hero-search');
const modal = document.getElementById('hero-modal');
const modalBody = document.getElementById('modal-body');
const closeModal = document.getElementById('close-modal');

let allHeroes = [];

async function init() {
  try {
    // Fetch all heroes
    allHeroes = await api.getHeroes();
    
    // Sort heroes by localized name
    allHeroes.sort((a, b) => a.name_loc.localeCompare(b.name_loc));
    
    renderHeroes(allHeroes);
    updateLastUpdateDate(allHeroes);
    
    // Setup search
    searchInput.addEventListener('input', (e) => {
      const query = e.target.value.toLowerCase();
      const filtered = allHeroes.filter(h => 
        h.name_loc.toLowerCase().includes(query) || 
        h.name.toLowerCase().includes(query)
      );
      renderHeroes(filtered);
    });

    // Setup modal close
    closeModal.onclick = () => modal.classList.remove('active');
    window.onclick = (e) => {
      if (e.target === modal.querySelector('.modal-overlay')) {
        modal.classList.remove('active');
      }
    };

  } catch (error) {
    console.error('Failed to initialize:', error);
    heroGrid.innerHTML = `<div class="error">Failed to load heroes. Please try again later.</div>`;
  }
}

function renderHeroes(heroes) {
  heroGrid.innerHTML = '';
  
  if (heroes.length === 0) {
    heroGrid.innerHTML = `<div class="no-results">No heroes found matching your search.</div>`;
    return;
  }

  heroes.forEach(hero => {
    const card = document.createElement('div');
    card.className = 'hero-card';
    
    const imgUrl = Dota2Datafeed.urls.heroImage(hero.name);
    
    card.innerHTML = `
      <img src="${imgUrl}" alt="${hero.name_loc}" loading="lazy">
      <div class="hero-card-info">
        <div class="hero-name">${hero.name_loc}</div>
      </div>
    `;
    
    card.onclick = () => showHeroDetails(hero.id);
    heroGrid.appendChild(card);
  });
}

function parseItemBuild(vdf) {
  const sections = [];
  const lines = vdf.split('\n');
  let currentSection = null;
  
  for (let line of lines) {
    line = line.trim();
    if (line.startsWith('"#DOTA_Item_Build_')) {
      currentSection = {
        title: line.replace(/"/g, '').replace('#DOTA_Item_Build_', '').replace(/_/g, ' '),
        items: []
      };
      sections.push(currentSection);
    } else if (line.startsWith('"item"') && currentSection) {
      const match = line.match(/"item"\s+"([^"]+)"/);
      if (match) {
        currentSection.items.push(match[1]);
      }
    }
  }
  return sections;
}

async function showHeroDetails(id) {
  modal.classList.add('active');
  modalBody.innerHTML = `
    <div class="loader">
      <div class="spinner"></div>
      <span>Fetching hero details...</span>
    </div>
  `;

  try {
    const hero = await api.getHeroData(id);
    if (!hero) throw new Error('Hero not found');

    const imgUrl = Dota2Datafeed.urls.heroImage(hero.name);
    const attrs = ['Strength', 'Agility', 'Intelligence', 'Universal'];
    const attrName = attrs[hero.primary_attr] || 'Unknown';
    const attrIcon = Dota2Datafeed.urls.attributeIcon(hero.primary_attr);

    // Try to fetch the local guide
    const heroShortName = hero.name.replace('npc_dota_hero_', '');
    let sections = [];
    try {
      const response = await fetch(`./itembuilds/default_${heroShortName}.txt`);
      if (response.ok) {
        const vdf = await response.text();
        sections = parseItemBuild(vdf);
      }
    } catch (e) {
      console.warn('Guide fetch failed', e);
    }

    const sectionsHtml = sections.length > 0 
      ? sections.map(s => `
          <div class="guide-block" style="margin-bottom: 25px;">
            <h4 style="text-transform: uppercase; font-size: 0.8rem; color: var(--accent-gold); margin-bottom: 12px; letter-spacing: 1px;">${s.title}</h4>
            <div class="item-list">
              ${s.items.map(item => `
                <div class="item-slot" title="${item.replace('item_', '').replace(/_/g, ' ')}">
                  <img src="${Dota2Datafeed.urls.itemImage(item)}" alt="${item}" onerror="this.src='https://cdn.cloudflare.steamstatic.com/apps/dota2/images/dota_react/items/recipe.png'">
                </div>
              `).join('')}
            </div>
          </div>
        `).join('')
      : `<p style="color: var(--text-dim);">No guide available for this hero.</p>`;

    modalBody.innerHTML = `
      <div class="hero-detail">
        <header class="hero-header">
          <img src="${imgUrl}" alt="${hero.name_loc}" class="hero-header-img">
          <div class="hero-info">
            <h2>${hero.name_loc}</h2>
            <div class="hero-attr">
              <img src="${attrIcon}" alt="${attrName}" class="attr-icon-img">
              ${attrName} Hero
            </div>
            <div class="hero-complexity" style="margin-top: 10px; color: var(--text-dim);">
              Complexity: ${'★'.repeat(hero.complexity)}${'☆'.repeat(3 - hero.complexity)}
            </div>
          </div>
        </header>
        
        <div class="guides-section">
          <h3>Generated Item Build</h3>
          <div class="item-build">
            ${sectionsHtml}
          </div>
        </div>
      </div>
    `;
  } catch (error) {
    modalBody.innerHTML = `<div class="error">Failed to load hero details.</div>`;
  }
}

init();
