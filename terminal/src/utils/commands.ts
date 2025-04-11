import packageJson from '../../package.json';
import themes from '../../themes.json';
import {history} from '../stores/history';
import {theme} from '../stores/theme';

const hostname = window.location.hostname;

export const commands: Record<string, (args: string[]) => Promise<string> | string> = {
  help: () => 'Available commands: ' + Object.keys(commands).join(', '),
  hostname: () => hostname,
  whoami: () => 'guest',
  date: () => new Date().toLocaleString(),
  vi: () => `why use vi? try 'emacs'`,
  vim: () => `why use vim? try 'emacs'`,
  emacs: () => `why use emacs? try 'vim'`,
  echo: (args: string[]) => args.join(' '),
  sudo: (args: string[]) => {
    window.open('https://www.youtube.com/watch?v=dQw4w9WgXcQ');

    return `Permission denied: unable to run the command '${args[0]}' as root.`;
  },
  theme: (args: string[]) => {
    const usage = `Usage: theme [args].
    [args]:
      ls: list all available themes
      set: set theme to [theme]

    [Examples]:
      theme ls
      theme set gruvboxdark
    `;
    if (args.length === 0) {
      return usage;
    }

    switch (args[0]) {
      case 'ls': {
        let result = themes.map((t) => t.name.toLowerCase()).join(',\n');
        result += `You can preview all these themes here: https://github.com/m4tt72/terminal/tree/main/docs/themes`;

        return result;
      }

      case 'set': {
        if (args.length !== 2) {
          return usage;
        }

        const selectedTheme = args[1];
        const t = themes.find((t) => t.name.toLowerCase() === selectedTheme);

        if (!t) {
          return `Theme '${selectedTheme}' not found. Try 'theme ls' to see all available themes.`;
        }

        theme.set(t);

        return `Theme set to ${selectedTheme}`;
      }

      default: {
        return usage;
      }
    }
  },
  repo: () => {
    window.open(packageJson.repository.url, '_blank');

    return 'Opening repository...';
  },
  jellyfin: () => {
    window.open('https://jellyfin.cloud417.space', '_blank');

    return 'Opening Jellyfin...';
  },
  torrent: () => {
    window.open('https://torrent.cloud417.space', '_blank');

    return 'Opening Torrent...';
  },
  profile: () => {
    window.open('https://github.com/Hamza417', '_blank');

    return 'Opening Profile...';
  },
  clear: () => {
    history.set([]);

    return '';
  },
  weather: async (args: string[]) => {
    const city = args.join('+');

    if (!city) {
      return 'Usage: weather [city]. Example: weather Brussels';
    }

    const weather = await fetch(`https://wttr.in/${city}?ATm`);

    return weather.text();
  },
  neofetch: async () => {
    try {
      const response = await fetch('/neofetch');
      if (!response.ok) {
        return `Error: Unable to fetch neofetch output.`;
      }
      return await response.text();
    } catch (error) {
      // @ts-ignore
      return `Error: ${error.message}`;
    }
  },
  exit: () => {
    return 'Please close the tab to exit.';
  },
  curl: async (args: string[]) => {
    if (args.length === 0) {
      return 'curl: no URL provided';
    }

    const url = args[0];

    try {
      const response = await fetch(url);
      return await response.text();
    } catch (error) {
      return `curl: could not fetch URL ${url}. Details: ${error}`;
    }
  },
  banner: () => `
  

$$\\   $$\\  $$$$$$\\  $$\\      $$\\ $$$$$$$$\\  $$$$$$\\  $$\\   $$\\   $$\\   $$$$$$$$\\ 
$$ |  $$ |$$  __$$\\ $$$\\    $$$ |\\____$$  |$$  __$$\\ $$ |  $$ |$$$$ |  \\____$$  |
$$ |  $$ |$$ /  $$ |$$$$\\  $$$$ |    $$  / $$ /  $$ |$$ |  $$ |\\_$$ |      $$  / 
$$$$$$$$ |$$$$$$$$ |$$\\$$\\$$ $$ |   $$  /  $$$$$$$$ |$$$$$$$$ |  $$ |     $$  /  
$$  __$$ |$$  __$$ |$$ \\$$$  $$ |  $$  /   $$  __$$ |\\_____$$ |  $$ |    $$  /   
$$ |  $$ |$$ |  $$ |$$ |\\$  /$$ | $$  /    $$ |  $$ |      $$ |  $$ |   $$  /    
$$ |  $$ |$$ |  $$ |$$ | \\_/ $$ |$$$$$$$$\\ $$ |  $$ |      $$ |$$$$$$\\ $$  /     
\\__|  \\__|\\__|  \\__|\\__|     \\__|\\________|\\__|  \\__|      \\__|\\______|\\__/      
                                                                                 
                                                                                 
Type 'help' to see list of available commands.
`,
};
