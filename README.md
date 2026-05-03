# AdSense Automation Site

Automated Hugo-based content site optimized for Google AdSense revenue.

## Quick Start

1. **Replace AdSense ID**: Replace `ca-pub-YOUR_PUBLISHER_ID` in `hugo.toml` with your actual publisher ID.

2. **Set up automation**:
   ```bash
   pip install -r automation/requirements.txt
   export OPENAI_API_KEY="your-key-here"
   python automation/generate_content.py
   ```

3. **Deploy to Netlify/Vercel**:
   - Push to GitHub
   - Connect repo to Netlify/Vercel
   - Set build command: `hugo`
   - Set publish directory: `public`

4. **Enable auto-generation**:
   - Add `OPENAI_API_KEY` to GitHub repo secrets
   - GitHub Actions will run every 6 hours

## High-CPM Niche Strategy

Target sub-niches with lower competition:
- "Life insurance for pilots" (CPC $28, competition 40/100)
- "EV car insurance rates 2026" (emerging trend)
- "Credit cards for college students" (CPC $20-40)
- "Telemedicine platform reviews" (CPC $25-45)

## Important Notes

- Write 15+ quality posts before applying to AdSense
- Include proper disclaimers (see about page)
- Never publish duplicate content
- Monitor Core Web Vitals in Google Search Console
