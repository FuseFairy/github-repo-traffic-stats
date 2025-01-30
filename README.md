
[![github-profile-repo-analytics][socialify-image]][github-profile-repo-analytics--url]

This project automates the process of fetching and visualizing traffic data for **your public GitHub repositories** using GitHub Actions. It periodically retrieves metrics like views and clones and generates traffic charts in SVG format. The generated charts can be easily embedded in your GitHub profile or repository to track project activity.

## ✨Features
- 🌐Fetch traffic data from GitHub repositories
- 📈Visualize traffic data with customizable charts
- 🎨Support for different themes and background colors
- 🔃Data is automatically refreshed every day

## 🌟Demo
Here’s an example of a traffic chart generated from a public GitHub repository:
```html
<div align="center">
  <img src="https://raw.githubusercontent.com/FuseFairy/github-profile-repo-analytics/output/generated/traffic_chart.svg" alt="Repos traffic stats" />
</div>
```
![Sample Chart](https://raw.githubusercontent.com/gist/FuseFairy/c7f619079a91afedbf4e949977fa2df4/raw/e868d3bc96ce8755d7f8beb1130e5d7579c9e2c0/demo-traffic.svg)

## 🚀How to Deploy Your Own Instance with GitHub Workflows
<details>
  <summary><strong>Click to expand deployment instructions</strong></summary>

  ### 1. Create a Personal Access Token
  - Go to [Personal access tokens (classic) page](https://github.com/settings/tokens).
  - Create a **Personal access tokens (classic)** with **repo** and **user** permissions to access repository stats.
  
  ### 2. Fork the Repository
  - Go to the GitHub repository for this project.
  - Click **Fork** in the upper-right corner to create your own copy.
  
  ### 3. Set Up GitHub Secrets
  - Go to your forked repository.
  - Navigate to **Settings** > **Secrets and Variables** > **Actions** > **New repository secret**.
  - Add the following secrets:
    - **TOKEN**: Your personal access token that you created in Step 1.
    - **USERNAME**: Your GitHub username.
  
  ### 4. Final
  - Go to the **Actions Page** and press "Run Workflow" on the right side of the screen to generate images for the first time.
  - Once complete, you can find the generated images in the  *generated folder* under the `output` branch.
  
</details>

## 🛠 Configuration (config.yml)
This file allows you to customize the appearance of the generated traffic chart. You can modify the theme, dimensions, colors, and exclude specific repositories.
```yaml
theme: "tokyo-night"  # The theme used for the chart. Available themes are defined in the "src/themes" folder.
height: 400  # The height of the chart in pixels.
width: 800  # The width of the chart in pixels.
radius: 20  # The corner radius for the chart's rectangular background.
ticks: 5  # The number of y-axis ticks on the chart.

bg_color: "#00000000"  # Background color of the chart in hex format. "#00000000" represents fully transparent black.
clones_color: null  # Stroke color for the clones line. Set to a hex value (e.g., "#FF5733") or leave as `null` for default.
views_color: null  # Stroke color for the views line. Set to a hex value (e.g., "#33FF57") or leave as `null` for default.
clones_point_color: null  # Color for the clone data points on the chart. Set to a hex value or leave as `null` for default.
views_point_color: null  # Color for the view data points on the chart. Set to a hex value or leave as `null` for default.

exclude_repos: ["repo_1", "repo_2"]  # A list of repository names to exclude from the chart. Set to `[]` to include all repositories.
```


## 🎨Available Themes

Here are the currently available themes you can use for your traffic charts. The themes are stored in the `src/themes` directory. Feel free to contribute and add your own themes by submitting a pull request!


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

[socialify-image]: https://raw.githubusercontent.com/gist/FuseFairy/c233e02ce0225b8db2a093bdb71a4de0/raw/5f816da3d6360fcd61074f485740a6bcff0b3acc/github-profile-repo-analytics.svg

[github-profile-repo-analytics--url]: https://github.com/FuseFairy/github-profile-repo-analytics
