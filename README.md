
[![github-profile-repo-analytics][socialify-image]][github-profile-repo-analytics--url]

This project provides an API for fetching and visualizing traffic data of **your public GitHub repositories**, including metrics like views and clones. It allows users to generate traffic charts in SVG format for their own repositories, helping developers and maintainers monitor the activity of their projects.

> [!NOTE]  
> Due to GitHub API limitations, you can only retrieve traffic data (such as views and clones) for the GitHub repositories you own through your own self-hosted API.

## ✨Features
- 🌐Fetch traffic data from GitHub repositories
- 📈Visualize traffic data with customizable charts
- 🎨Support for different themes and background colors
- 🔃Data is automatically refreshed every 2 hours

## 🌟Demo
Here’s an example of a traffic chart generated from a public GitHub repository:
```
![Sample Chart](https://github-profile-repo-analytics.vercel.app/api?theme=tokyo-night&bg_color=00000000)
```
![Sample Chart](https://raw.githubusercontent.com/gist/FuseFairy/c7f619079a91afedbf4e949977fa2df4/raw/e868d3bc96ce8755d7f8beb1130e5d7579c9e2c0/demo-traffic.svg)

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
  
  ### 5. Set Vercel Environment Variables
  - Add a new environment variable when Configure Project:
    - **Name**: `GITHUB_TOKEN`
      - **Value**: Your personal access token
    - **Name**: `GITHUB_USERNAME`
      - **Value**: Your github username
  
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
  git clone https://github.com/FuseFairy/github-profile-repo-analytics.git
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
  GITHUB_USERNAME=<your_github_username>
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
| `theme`         | `string` | The theme for the chart. Available options: `default`, `tokyo-night`, etc.                                 | `default`      | ❌      |
| `bg_color`      | `string` | Background color of the chart in hex format (e.g., `FFFFFF` for white, `00000000` for transparent black).  | None           | ❌      |
| `clones_color`      | `string` | Color of the clones stroke in hex format (e.g., `FFFFFF` for white, `00000000` for transparent black).  | None           | ❌      |
| `views_color`      | `string` | Color of the views stroke in hex format (e.g., `FFFFFF` for white, `00000000` for transparent black).  | None           | ❌      |
| `clones_point_color`      | `string` | Color of the clones point in hex format (e.g., `FFFFFF` for white, `00000000` for transparent black).  | None           | ❌      |
| `views_point_color`      | `string` | Color of the views point in hex format (e.g., `FFFFFF` for white, `00000000` for transparent black).  | None           | ❌      |
| `radius`      | `integer` | Corner radius for the chart's rectangular background.  | `20`           | ❌      |
| `height`        | `integer`| Height of the chart in pixels **(minimum: 400)**.                                                          | `400`          | ❌      |
| `width`         | `integer`| Width of the chart in pixels **(minimum: 800)**.                                                           | `800`          | ❌      |
| `exclude_repos` | `string` | A comma-separated list of repository names to exclude from the traffic data.                               | None           | ❌      |
| `ticks` | `integer` | The desired number of evenly spaced markers on the y-axis to improve chart readability. The actual number may vary slightly based on data. **(minimum: 5)**                           | `5`          | ❌      |

**Usage Examples**

Here are some example API calls to demonstrate usage:
- Custom Chart Theme and Background
  ```
  /api?theme=tokyo-night&bg_color=00000000
  ```
- Modify the Stroke Color Directly
  ```
  /api?clones_color=8ab0c6&views_color=c6c6c6
  ```
- Exclude Specific Repositories
  ```
  /api?exclude_repos=temp,example-repo
  ```
- Custom Chart Size
  ```
  /api?height=600&width=1000
  ```
> [!TIP]
> Use the interactive documentation at `/docs` to explore the API easily.

## 🎨Available Themes

Here are the currently available themes you can use for your traffic charts. The themes are stored in the `app/themes` directory. Feel free to contribute and add your own themes by submitting a pull request!


| Theme | Preview | Theme | Preview  |
|---------------|-----------------|---------------|---------|
| `default`     | <img src="https://raw.githubusercontent.com/gist/FuseFairy/55338818fc1344253b696d803d35e71c/raw/31c11a392dc7aa3535d05e9785b566b2dbbebb21/default-traffic.svg" alt="Default Theme" width="250" />  | `cyberpunk` | <img src="https://raw.githubusercontent.com/gist/FuseFairy/9db14fc42f2cd48236e4758ceece730d/raw/533b3ce07c81478cad3038a5ebf3deb857b399b0/cyberpunk-traffic.svg" alt="Cyberpunk Theme" width="250" /> |
| `dark-mode`   | <img src="https://raw.githubusercontent.com/gist/FuseFairy/7a2d9a5c6dec369455ab0e42cb49aca8/raw/8ff0de46b5f29f73c20765dba869da110a85258b/dark-mode-traffic.svg" alt="Dark Mode Theme" width="250" /> | `ocean-depth` | <img src="https://raw.githubusercontent.com/gist/FuseFairy/4bda8dc6f0ef3586dca7795928b2d63d/raw/d9b96212facecf957d6a58c7a65d46be36b7051d/ocean-depth-traffic.svg" alt="Ocean Depth Theme" width="250" /> |
| `spring-fresh`| <img src="https://raw.githubusercontent.com/gist/FuseFairy/18d2ce24fe2ce4141a1d29a7d7294bdc/raw/e27c334861808f1e333353fd6d31c029025d08b5/spring-fresh-traffic.svg" alt="Spring Fresh Theme" width="250" /> | `tokyo-night` | <img src="https://raw.githubusercontent.com/gist/FuseFairy/89fa84f331c4fa7e812c59e2e0df06ce/raw/fce3445fded9ef0a703adb3d8c67ed7ffed2a75a/tokyo-night-traffic.svg" alt="Tokyo Night Theme" width="250" /> |


### How to Add Your Own Theme 🖌️

1. Create a new JSON file for your theme in the `app/themes` directory.
2. **Follow the existing structure**:  
    Your theme JSON should follow this structure, where you can customize the `background_color`, `line_colors`, `text_color`, and `grid_color` for your theme:

    ```json
    {
      "background_color": "#1a1b27",
      "line_colors": {
        "clones": "#8aadf466",
        "views": "#cba6f766"
      },
      "point_colors": {
        "clones": "#8aadf4",
        "views": "#cba6f7"
      },
      "text_color": "#cdd6f4",
      "grid_color": "#414868"
    }
    ```

3. Submit a pull request with your new theme.

Your contribution will help make this project even better! 🚀

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/FuseFairy/github-repo-traffic-stats/blob/main/LICENSE) file for details.

[socialify-image]: https://raw.githubusercontent.com/gist/FuseFairy/c233e02ce0225b8db2a093bdb71a4de0/raw/f0c4137fa0dcc0d0997848613b6fbe61935f2e00/github-profile-repo-analytics.svg

[github-profile-repo-analytics--url]: https://github.com/FuseFairy/github-profile-repo-analytics
