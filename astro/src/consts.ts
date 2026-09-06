// Place any global data in this file.
// You can import this data from anywhere in your site by using the `import` keyword.

export const SITE_TITLE = 'Silvio Fanzon';
export const SITE_DESCRIPTION = 'Applied mathematician working across modelling, optimisation, statistics and scientific computing.';

export const CV_URL = '/Silvio_Fanzon_Academic_CV.pdf';

export const CONTACT = {
  organization: 'Silvio Fanzon',
  addressLines: [
    'Applied Mathematician',
  ],
  emails: [
    'silvio.fanzon.work@gmail.com',
  ],
};

export type SocialIcon = 'website' | 'scholar' | 'email' | 'github' | 'linkedin' | 'twitter';

export const SOCIAL_LINKS: ReadonlyArray<{
  label: string;
  href: string;
  icon: SocialIcon;
}> = [
  {
    label: 'GitHub',
    href: 'https://github.com/sfanzon',
    icon: 'github',
  },
  {
    label: 'Email',
    href: 'mailto:silvio.fanzon.work@gmail.com',
    icon: 'email',
  },
  {
    label: 'LinkedIn',
    href: 'https://www.linkedin.com/in/fanzon',
    icon: 'linkedin',
  },
  {
    label: 'Scholar',
    href: 'https://scholar.google.com/citations?user=9yJyLsoAAAAJ',
    icon: 'scholar',
  },
];

export const FOOTER_CREDIT = {
  designerName: 'Silvio Fanzon',
  designerUrl: 'https://www.silviofanzon.com',
  sourceLabel: 'Source code',
  sourceUrl: 'https://github.com/sfanzon',
};

// Umami analytics — configured via environment variables so no tracking ID is
// committed. Set PUBLIC_UMAMI_WEBSITE_ID (e.g. in a .env file or a CI variable)
// to enable it; leave it unset to disable analytics entirely.
export const UMAMI_SRC = import.meta.env.PUBLIC_UMAMI_SRC ?? 'https://cloud.umami.is/script.js';
export const UMAMI_WEBSITE_ID = import.meta.env.PUBLIC_UMAMI_WEBSITE_ID ?? '';
