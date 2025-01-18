# 📊GitHub Repo Traffic Stats

This project provides an API for fetching and visualizing traffic data of **your GitHub repositories**, including metrics like views and clones. It allows users to generate traffic charts in SVG format for their own repositories, helping developers and maintainers monitor the activity of their projects.

## ✨Features
- 🌐Fetch traffic data from GitHub repositories
- 📈Visualize traffic data with customizable charts
- 🎨Support for different themes and background colors
- 🔃Data is automatically refreshed every 24 hours

## 🌟Demo
Here’s an example of a traffic chart generated from a public GitHub repository:
```
![Sample Chart](https://github-repo-traffic-stats.vercel.app/api?username=FuseFairy&theme=tokyo-night&bg_color=00000000)
```
![Sample Chart](https://github-repo-traffic-stats.vercel.app/api?username=FuseFairy&theme=tokyo-night&bg_color=00000000)

## 🚀How to Deploy Your Own Instance on Vercel
<details>
  <summary><strong>Click to expand deployment instructions</strong></summary>

  ### 1. Sign in to Vercel
  - Visit [vercel.com](https://vercel.com).
  - Click **Log in** and choose **Continue with GitHub**.
  - Authorize Vercel to access your GitHub account if prompted.
  
  ### 2. Fork the Repository
  - Go to the GitHub repository for this project.
  - Click **Fork** in the upper-right corner to create your own copy.
  
  ### 3. Import the Project to Vercel
  - Go to your Vercel dashboard.
  - Click **New Project**, then choose **Continue with GitHub**.
  - Find the forked repository and click **Import**.
    - Alternatively, you can import a third-party repository by selecting **Import Third-Party Git Repository**.
  
  ### 4. Create a Personal Access Token
  - Go to [Personal access tokens (classic) page](https://github.com/settings/tokens).
  - Create a **Personal access tokens (classic)** with **repo** and **user** permissions to access repository stats.
  
  ### 5. Set the Personal Access Token in Vercel Environment Variables
  - Add a new environment variable when Configure Project:
    - **Name**: `GITHUB_TOKEN`
    - **Value**: Your personal access token
  
  ### 6. Deploy the Project
  - Click **Deploy** in Vercel and wait for the deployment process to finish.
  - Once complete, you can find your project’s domain under the **Domains** section in the Vercel dashboard.
  
  ### 7. Use the API
  - The API is now live! You can start using it by accessing the provided domain to fetch and display traffic data for your GitHub repositories.
</details>

## 💻Setting Up Local Development
<details> 
  <summary><strong>Click to expand local development instructions</strong></summary>

  **Python 3.12+** is required to run this project.

  ### 1. Clone the Repository
  ```
  git clone https://github.com/FuseFairy/github-repo-traffic-stats.git
  ```

  ### 2. Navigate to the Project Directory
  ```
  cd github-repo-traffic-stats
  ```

  ### 3. Install Dependencies
  ```
  pip install -r requirements.txt
  pip install uvicorn
  ```

  ### 4. Set Up Environment Variables
  Create a `.env` file in the project directory and add your **GitHub Personal Access Token**
  ```
  GITHUB_TOKEN=<your_personal_access_token>
  ```

  ### 5. Run the Application
  Start the FastAPI server locally:
  ```
  uvicorn app.main:app --reload
  ```
  By default, the application will be available at `http://127.0.0.1:8000` (localhost on port 8000).
  
  If you've modified the `--host` or `--port` parameters in the command, the server will run on the specified address and port. Adjust your browser or API client accordingly. For example:
  ```
  uvicorn app.main:app --host 0.0.0.0 --port 9000
  ```
  The application would then be accessible at `http://<your-ip>:9000`.
  
  ### 6. Test the API
  Open your browser or an API client like Postman to test the API.
  - The API base URL will be the same as the one configured in your uvicorn command.
  - Access the API documentation at `/docs` (e.g., `http://127.0.0.1:8000/docs`) to interact with the available endpoints.
</details>

## 📋API Parameters
The GitHub Repo Traffic Stats API allows users to customize their queries with the following parameters:

**Base URL**
- The API endpoint is:
  ```
  /api
  ```
- Example: `https://your-vercel-deployment-url.vercel.app/api`

**Parameters**
| Parameter       | Type     | Description                                                                                                | Default Value  | Required |
|-----------------|----------|------------------------------------------------------------------------------------------------------------|----------------|----------|
| `username`      | `string` | Your GitHub username.                                                                                      | None           | ✅      |
| `theme`         | `string` | The theme for the chart. Available options: `default`, `tokyo-night`, etc.                                 | `default`      | ❌      |
| `bg_color`      | `string` | Background color of the chart in hex format (e.g., `FFFFFF` for white, `00000000` for transparent black).  | None           | ❌      |
| `clones_color`      | `string` | Color of the clones stroke in hex format (e.g., `FFFFFF` for white, `00000000` for transparent black).  | None           | ❌      |
| `views_color`      | `string` | Color of the views stroke in hex format (e.g., `FFFFFF` for white, `00000000` for transparent black).  | None           | ❌      |
| `height`        | `integer`| Height of the chart in pixels **(minimum: 400)**.                                                          | `400`          | ❌      |
| `width`         | `integer`| Width of the chart in pixels **(minimum: 800)**.                                                           | `800`          | ❌      |
| `exclude_repos` | `string` | A comma-separated list of repository names to exclude from the traffic data.                               | None           | ❌      |

**Usage Examples**

Here are some example API calls to demonstrate usage:
- Basic Request
  ```
  /api?username=fusefairy
  ```
- Custom Chart Theme and Background
  ```
  /api?username=fusefairy&theme=tokyo-night&bg_color=00000000
  ```
- Modify the Stroke Color Directly
  ```
  /api?username=fusefairy&clones_color=8ab0c6&views_color=c6c6c6
  ```
- Exclude Specific Repositories
  ```
  /api?username=fusefairy&exclude_repos=temp,example-repo
  ```
- Custom Chart Size
  ```
  /api?username=fusefairy&height=600&width=1000
  ```
> [!TIP]
> Use the interactive documentation at `/docs` to explore the API easily.

## 🎨Available Themes

Here are the currently available themes you can use for your traffic charts. The themes are stored in the `app/themes` directory. Feel free to contribute and add your own themes by submitting a pull request!


| Theme | Preview | Theme | Preview  |
|---------------|-----------------|---------------|---------|
| `default`     | <img src="https://github-repo-traffic-stats.vercel.app/api?username=FuseFairy&theme=default" alt="Default Theme" width="300" />  | `cyberpunk` | <img src="https://github-repo-traffic-stats.vercel.app/api?username=FuseFairy&theme=cyberpunk" alt="Cyberpunk Theme" width="300" /> |
| `dark-mode`   | <img src="https://github-repo-traffic-stats.vercel.app/api?username=FuseFairy&theme=dark-mode" alt="Dark Mode Theme" width="300" /> | `ocean-depth` | <img src="https://github-repo-traffic-stats.vercel.app/api?username=FuseFairy&theme=ocean-depth" alt="Ocean Depth Theme" width="300" /> |
| `spring-fresh`| <img src="https://github-repo-traffic-stats.vercel.app/api?username=FuseFairy&theme=spring-fresh" alt="Spring Fresh Theme" width="300" /> | `tokyo-night` | <img src="https://github-repo-traffic-stats.vercel.app/api?username=FuseFairy&theme=tokyo-night" alt="Tokyo Night Theme" width="300" /> |


### How to Add Your Own Theme 🖌️

1. Create a new JSON file for your theme in the `app/themes` directory.
2. **Follow the existing structure**:  
   Your theme JSON should follow this structure, where you can customize the `background_color`, `line_colors`, `text_color`, and `grid_color` for your theme:

   ```json
   {
      "background_color": "rgba(0, 26, 51, 1)",
      "line_colors": {
        "clones": "rgba(0, 204, 255, 1)",
        "views": "rgba(0, 255, 204, 1)"
      },
      "text_color": "rgba(255, 255, 255, 1)",
      "grid_color": "rgba(30, 58, 81, 1)"
   }
3. Submit a pull request with your new theme.

Your contribution will help make this project even better! 🚀

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/FuseFairy/github-repo-traffic-stats/blob/main/LICENSE) file for details.
