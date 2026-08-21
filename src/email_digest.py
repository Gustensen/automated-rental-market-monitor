from html import escape
from urllib.parse import quote_plus


def build_maps_link(address):
		"""
		Build a Google Maps search URL for the given address.
		RentCast does not include source listing URLs, so this gives
		a quick way to open the location from the digest email.
		"""
		# quote_plus handles spaces and special characters safely for a query string.
		encoded_address = quote_plus(address or "")
		return f"https://www.google.com/maps/search/?api=1&query={encoded_address}"


def build_digest_html(new_listings):
		"""
		Convert newly discovered listings into an HTML email body.
		Returns None when there are no new listings so callers can skip sending email.
		"""
		if not new_listings:
				return None

		rows = []
		for listing in new_listings:
				address = listing.get("formattedAddress") or "N/A"
				price = listing.get("price")
				beds = listing.get("bedrooms")
				baths = listing.get("bathrooms")
				agent = listing.get("listingAgent") or {}

				# Escape user/data-source strings to avoid broken HTML rendering.
				safe_address = escape(str(address))
				safe_agent_name = escape(str(agent.get("name") or "N/A"))
				safe_agent_phone = escape(str(agent.get("phone") or "N/A"))

				price_text = f"${int(price):,}" if isinstance(price, (int, float)) else "N/A"
				beds_text = str(beds) if beds is not None else "N/A"
				baths_text = str(baths) if baths is not None else "N/A"

				maps_link = build_maps_link(address)
				row = f"""
						<tr>
								<td>{safe_address}</td>
								<td>{price_text}</td>
								<td>{beds_text}bed/{baths_text}baths</td>
								<td><a href=\"{maps_link}\" target=\"_blank\" rel=\"noopener noreferrer\">Open Map</a></td>
								<td>{safe_agent_name}<br>{safe_agent_phone}</td>
						</tr>
				"""
				rows.append(row)

		# Keep styling inline so email clients render the table consistently.
		return f"""
		<html>
			<body style=\"font-family: Arial, sans-serif;\">
				<h2>New Rental Matches</h2>
				<p>Found {len(new_listings)} new listing(s) this run.</p>
				<table border=\"1\" cellpadding=\"8\" cellspacing=\"0\" style=\"border-collapse: collapse;\">
					<thead style=\"background-color: #f2f2f2;\">
						<tr>
							<th>Address</th>
							<th>Price</th>
							<th>Beds/Baths</th>
							<th>Map link</th>
							<th>Agent name + phone</th>
						</tr>
					</thead>
					<tbody>
						{''.join(rows)}
					</tbody>
				</table>
			</body>
		</html>
		"""
