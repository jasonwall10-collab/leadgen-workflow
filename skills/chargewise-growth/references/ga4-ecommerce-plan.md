# GA4 ecommerce plan (minimum viable tracking)

## Foundations
- Ensure GA4 is installed via GTM or site tag.
- Link GA4 ↔ Google Ads (if running ads).
- Link GA4 ↔ Search Console.

## Ecommerce events (baseline)
- view_item_list
- select_item
- view_item
- add_to_cart
- view_cart
- begin_checkout
- add_shipping_info
- add_payment_info
- purchase

## Key events (conversions)
- purchase (primary)
- begin_checkout / add_to_cart (micro)
- generate_lead / contact (if applicable)

## Reports to build
- Funnel: product view → add to cart → checkout → purchase
- Landing page performance (organic vs paid)
- Top queries (from GSC) mapped to landing pages

## Questions to answer weekly
- Which landing pages bring qualified traffic?
- What products convert best by channel/device?
- Where is the biggest funnel drop?

Source (setup basics): https://support.google.com/analytics/answer/9304153
