import dns.resolver
import dns.reversename
from typing import List, Dict, Any
from url_analyzer.core.base_analyzer_interface import BaseAnalyzer
from url_analyzer.utils.exceptions import DNSAnalyzerError

class DNSAnalyzer(BaseAnalyzer):
    """DNS record analyzer."""

    def __init__(self, domain: str):
        self.domain = domain
        try:
            self.resolver = dns.resolver.Resolver()
        except:
            # Handle Termux case where /etc/resolv.conf doesn't exist
            self.resolver = dns.resolver.Resolver(configure=False)
        # Use Google's public DNS servers
        self.resolver.nameservers = ['8.8.8.8', '8.8.4.4']

    def get_info(self) -> Dict[str, Any]:
        """Get basic DNS information."""
        return {
            "domain": self.domain,
            "nameservers": self.resolver.nameservers
        }

    def _resolve(self, record_type: str) -> List[Any]:
        """Internal method to resolve DNS records.
        
        Args:
            record_type: Type of DNS record (A, AAAA, MX, etc.)
            
        Returns:
            List of DNS answers
            
        Raises:
            DNSAnalyzerError: If DNS query fails
        """
        try:
            return self.resolver.resolve(self.domain, record_type)
        except Exception as e:
            raise DNSAnalyzerError(f"Failed to get {record_type} records: {str(e)}")

    def get_a_records(self) -> List[str]:
        """Get IPv4 address records."""
        try:
            answers = self._resolve("A")
            return [answer.address for answer in answers]
        except DNSAnalyzerError:
            return []

    def get_aaaa_records(self) -> List[str]:
        """Get IPv6 address records."""
        try:
            answers = self._resolve("AAAA")
            return [answer.address for answer in answers]
        except DNSAnalyzerError:
            return []

    def get_cname_records(self) -> List[str]:
        """Get canonical name records."""
        try:
            answers = self._resolve("CNAME")
            return [str(answer.target) for answer in answers]
        except DNSAnalyzerError:
            return []

    def get_mx_records(self) -> List[Dict[str, Any]]:
        """Get mail exchange records."""
        try:
            answers = self._resolve("MX")
            return [{
                "exchange": str(answer.exchange),
                "preference": answer.preference
            } for answer in answers]
        except DNSAnalyzerError:
            return []

    def get_txt_records(self) -> List[str]:
        """Get text records."""
        try:
            answers = self._resolve("TXT")
            return [str(string.decode()) for answer in answers 
                   for string in answer.strings]
        except DNSAnalyzerError:
            return []

    def get_ns_records(self) -> List[str]:
        """Get name server records."""
        try:
            answers = self._resolve("NS")
            return [str(answer.target) for answer in answers]
        except DNSAnalyzerError:
            return []

    def get_soa_record(self) -> Dict[str, Any]:
        """Get start of authority record."""
        try:
            answers = self._resolve("SOA")
            soa = answers[0]
            return {
                "mname": str(soa.mname),
                "rname": str(soa.rname),
                "serial": soa.serial,
                "refresh": soa.refresh,
                "retry": soa.retry,
                "expire": soa.expire,
                "minimum": soa.minimum
            }
        except DNSAnalyzerError:
            return {}

    def analyze(self) -> Dict[str, Any]:
        """Perform complete DNS analysis."""
        result = {
            "info": self.get_info(),
            "records": {
                "a_records": self.get_a_records(),
                "aaaa_records": self.get_aaaa_records(),
                "cname_records": self.get_cname_records(),
                "mx_records": self.get_mx_records(),
                "txt_records": self.get_txt_records(),
                "ns_records": self.get_ns_records(),
                "soa_record": self.get_soa_record()
            }
        }
        return result
